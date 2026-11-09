from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from commons.testing import create_user

from .models import Destination, SiteContent

SECTIONS = [
    {
        "title": "Wunschliste",
        "items": [
            {"icon": "japan", "label": "Japan", "iconSet": "countries"},
            {"icon": "scotland", "label": "Schottland", "iconSet": "countries"},
        ],
    },
    {
        "title": "Bereiste Länder",
        "items": [{"icon": "switzerland", "label": "Schweiz", "iconSet": "countries"}],
    },
]


class CountryMapTests(APITestCase):
    def setUp(self):
        SiteContent.objects.update_or_create(
            key="countries", defaults={"data": SECTIONS}
        )
        self.viewer = create_user("viewer", "view_countries")
        self.editor = create_user("editor", "view_countries", "change_countries")

    def test_locates_countries_by_code_or_point(self):
        self.client.force_authenticate(self.viewer)
        wishlist = self.client.get("/api/content/countries/map/").data["sections"][0]

        japan, scotland = wishlist["countries"]
        self.assertEqual(japan["code"], "392")
        self.assertIsNone(japan["point"])
        self.assertIsNone(scotland["code"])
        self.assertEqual(scotland["point"], [-4.2, 56.8])

    def test_requires_view_permission(self):
        self.client.force_authenticate(create_user("stranger"))
        response = self.client.get("/api/content/countries/map/")
        self.assertEqual(response.status_code, 403)

    def test_destination_counts_days_left(self):
        day = timezone.localdate() + timedelta(days=30)
        self.client.force_authenticate(self.editor)
        response = self.client.put(
            "/api/content/countries/destination/",
            {"icon": "japan", "date": day.isoformat()},
            format="json",
        )

        destination = response.data["destination"]
        self.assertEqual(destination["label"], "Japan")
        self.assertEqual((destination["section"], destination["item"]), (0, 0))
        self.assertEqual(destination["days_left"], 30)

    def test_destination_without_date(self):
        self.client.force_authenticate(self.editor)
        response = self.client.put(
            "/api/content/countries/destination/", {"icon": "japan"}, format="json"
        )
        self.assertIsNone(response.data["destination"]["days_left"])

    def test_rejects_unlisted_destination(self):
        self.client.force_authenticate(self.editor)
        response = self.client.put(
            "/api/content/countries/destination/", {"icon": "peru"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_hides_destination_removed_from_lists(self):
        Destination.objects.create(icon="peru")
        self.client.force_authenticate(self.viewer)
        response = self.client.get("/api/content/countries/map/")
        self.assertIsNone(response.data["destination"])

    def test_viewer_cannot_set_destination(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.put(
            "/api/content/countries/destination/", {"icon": "japan"}, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_clearing_destination(self):
        Destination.objects.create(icon="japan")
        self.client.force_authenticate(self.editor)
        response = self.client.delete("/api/content/countries/destination/")
        self.assertIsNone(response.data["destination"])


NEWS = [
    {
        "title": "Medien",
        "items": [
            {"key": "news", "groups": []},
            {
                "key": "apps",
                "privacy": {"title": "Privacy-Faktor"},
                "groups": [
                    {
                        "title": "Ersetzt",
                        "items": [
                            {
                                "name": "Brave",
                                "country": "united_states",
                                "footprint": 2,
                                "replaces": [
                                    {
                                        "name": "Chrome",
                                        "country": "united_states",
                                        "footprint": 8,
                                    }
                                ],
                            },
                            {
                                "name": "Brave",
                                "country": "united_states",
                                "footprint": 2,
                                "replaces": [
                                    {
                                        "name": "Safari",
                                        "country": "united_states",
                                        "footprint": 4,
                                    }
                                ],
                            },
                            {
                                "name": "FreeTube",
                                "footprint": 1,
                                "replaces": [
                                    {
                                        "name": "YouTube",
                                        "country": "united_states",
                                        "footprint": 8,
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "title": "Nächste Schritte",
                        "items": [
                            {
                                "name": "GrapheneOS",
                                "country": "canada",
                                "footprint": 1,
                                "planned": True,
                                "replaces": [
                                    {
                                        "name": "Brave",
                                        "country": "united_states",
                                        "footprint": 2,
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "title": "Verzichtet",
                        "items": [
                            {
                                "name": "TikTok",
                                "country": "china",
                                "footprint": 10,
                                "dropped": True,
                            }
                        ],
                    },
                ],
            },
        ],
    }
]


class FootprintTests(APITestCase):
    def setUp(self):
        SiteContent.objects.update_or_create(key="news", defaults={"data": NEWS})

    def test_sums_unique_services_before_and_after(self):
        data = self.client.get("/api/content/news/footprint/").data
        self.assertEqual((data["before"]["value"], data["before"]["max"]), (30, 40))
        self.assertEqual((data["after"]["value"], data["after"]["max"]), (3, 40))
        self.assertEqual(data["reduction"], 90)

    def test_weights_countries_against_peak_before(self):
        data = self.client.get("/api/content/news/footprint/").data
        before = {country["icon"]: country for country in data["before"]["countries"]}
        after = {country["icon"]: country for country in data["after"]["countries"]}
        self.assertEqual(before["united_states"]["weight"], 1)
        self.assertEqual(before["united_states"]["code"], "840")
        self.assertAlmostEqual(before["china"]["weight"], 0.25 + 0.75 * 10 / 20)
        self.assertAlmostEqual(after["united_states"]["weight"], 0.25 + 0.75 * 2 / 20)
        self.assertEqual(after["united_states"]["label"], "Brave")

    def test_shares_include_services_without_country(self):
        data = self.client.get("/api/content/news/footprint/").data
        after = {country["icon"]: country for country in data["after"]["countries"]}
        self.assertEqual(after["united_states"]["share"], 67)
        self.assertEqual(after[None]["share"], 33)
        self.assertIsNone(after[None]["code"])

    def test_groups_eu_members_into_one_region(self):
        SiteContent.objects.filter(key="news").update(
            data=[
                {
                    "title": "Medien",
                    "items": [
                        {
                            "key": "apps",
                            "privacy": {"title": "Privacy-Faktor"},
                            "groups": [
                                {
                                    "title": "Ersetzt",
                                    "items": [
                                        {
                                            "name": "Qobuz",
                                            "country": "france",
                                            "footprint": 3,
                                            "replaces": [
                                                {
                                                    "name": "Spotify",
                                                    "country": "sweden",
                                                    "footprint": 6,
                                                }
                                            ],
                                        },
                                        {
                                            "name": "Codeberg",
                                            "country": "germany",
                                            "footprint": 1,
                                            "replaces": [
                                                {
                                                    "name": "GitHub",
                                                    "country": "united_states",
                                                    "footprint": 5,
                                                }
                                            ],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        )
        data = self.client.get("/api/content/news/footprint/").data
        after = {region["icon"]: region for region in data["after"]["regions"]}
        self.assertEqual(list(after), ["european_union"])
        self.assertEqual(after["european_union"]["label"], "Qobuz, Codeberg")
        self.assertEqual(after["european_union"]["share"], 100)
        countries = {country["icon"] for country in data["after"]["countries"]}
        self.assertEqual(countries, {"france", "germany"})
        self.assertEqual(data["flags"]["sweden"], "european_union")
        self.assertEqual(data["flags"]["united_states"], "united_states")

    def test_ignores_planned_steps(self):
        data = self.client.get("/api/content/news/footprint/").data
        icons = {country["icon"] for country in data["after"]["countries"]}
        self.assertNotIn("canada", icons)

    def test_missing_privacy_section(self):
        SiteContent.objects.filter(key="news").update(data=[])
        response = self.client.get("/api/content/news/footprint/")
        self.assertEqual(response.status_code, 404)


DASHBOARD_CV = [
    {
        "items": [
            {
                "key": "professional",
                "label": "Beruflicher Werdegang",
                "timeline": [
                    {"year": "2021", "title": "4teamwork AG", "description": "EFZ"},
                    {"year": "2999", "title": "Zukunft"},
                ],
            }
        ]
    }
]

DASHBOARD_NEWS = [
    {
        "items": [
            {
                "key": "news",
                "groups": [{"items": [{"name": "SRF", "url": "https://www.srf.ch"}]}],
            },
            {
                "key": "apps",
                "groups": [
                    {
                        "items": [
                            {
                                "name": "Signal",
                                "replaces": [{"name": "WhatsApp", "icon": "whatsapp"}],
                            },
                            {"name": "Ohne Ersatz"},
                        ]
                    }
                ],
            },
        ]
    }
]


class DashboardTests(APITestCase):
    def setUp(self):
        SiteContent.objects.update_or_create(key="cv", defaults={"data": DASHBOARD_CV})
        SiteContent.objects.update_or_create(
            key="news", defaults={"data": DASHBOARD_NEWS}
        )
        SiteContent.objects.update_or_create(
            key="now", defaults={"data": [{"label": "Arbeite an", "value": "ATLAS"}]}
        )

    def stats(self, response):
        return {stat["label"]: stat for stat in response.data["stats"]}

    def test_guest_sees_now_without_retrospect(self):
        response = self.client.get("/api/content/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["now"], [{"label": "Arbeite an", "value": "ATLAS"}]
        )
        self.assertIsNone(response.data["retrospect"])

    def test_cv_viewer_sees_past_retrospect(self):
        self.client.force_authenticate(create_user("viewer", "view_cv"))
        response = self.client.get("/api/content/dashboard/")
        self.assertEqual(response.data["retrospect"]["title"], "4teamwork AG")
        self.assertEqual(
            response.data["retrospect"]["years_ago"], timezone.localdate().year - 2021
        )

    def test_alternative_only_from_items_with_replacements(self):
        response = self.client.get("/api/content/dashboard/")
        self.assertEqual(response.data["alternative"]["name"], "Signal")
        self.assertEqual(self.stats(response)["Alternative"]["value"], 1)

    def test_medium_from_news_section(self):
        response = self.client.get("/api/content/dashboard/")
        self.assertEqual(response.data["medium"]["name"], "SRF")


def png(size=(4, 4)):
    from io import BytesIO

    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image as PillowImage

    output = BytesIO()
    PillowImage.new("RGB", size, "red").save(output, format="PNG")
    return SimpleUploadedFile("bild.png", output.getvalue(), content_type="image/png")


class SiteContentTests(APITestCase):
    def setUp(self):
        contents = {
            "impressum": {"text": "Hallo"},
            "cv": [{"title": "Werdegang"}],
            "media": [
                {"title": "Öffentlich", "items": []},
                {"title": "Arbeit", "requiresAuth": True, "items": []},
            ],
        }
        for key, data in contents.items():
            SiteContent.objects.update_or_create(key=key, defaults={"data": data})

    def test_public_content_is_readable(self):
        response = self.client.get("/api/content/impressum/")
        self.assertEqual(response.data["data"], {"text": "Hallo"})

    def test_restricted_content_needs_permission(self):
        self.assertEqual(self.client.get("/api/content/cv/").status_code, 403)
        self.client.force_authenticate(create_user("viewer", "view_cv"))
        self.assertEqual(self.client.get("/api/content/cv/").status_code, 200)

    def test_media_hides_work_groups_without_permission(self):
        titles = [
            group["title"]
            for group in self.client.get("/api/content/media/").data["data"]
        ]
        self.assertEqual(titles, ["Öffentlich"])
        self.client.force_authenticate(create_user("worker", "view_media"))
        titles = [
            group["title"]
            for group in self.client.get("/api/content/media/").data["data"]
        ]
        self.assertEqual(titles, ["Öffentlich", "Arbeit"])

    def test_unknown_content_is_missing(self):
        self.assertEqual(self.client.get("/api/content/unbekannt/").status_code, 404)

    def test_editing_needs_permission(self):
        self.client.force_authenticate(create_user("viewer", "view_cv"))
        response = self.client.put("/api/content/cv/", {"data": []}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_editor_saves_and_creates_content(self):
        self.client.force_authenticate(
            create_user("editor", "change_cv", "change_sitecontent")
        )
        response = self.client.put(
            "/api/content/cv/", {"data": [{"title": "Neu"}]}, format="json"
        )
        self.assertEqual(response.data["data"], [{"title": "Neu"}])
        response = self.client.put("/api/content/now/", {"data": []}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SiteContent.objects.filter(key="now").exists())


class UploadTests(APITestCase):
    def setUp(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        from django.test import override_settings

        self.root = TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        self.enterContext(override_settings(MEDIA_ROOT=Path(self.root.name)))

    def test_upload_needs_write_permission(self):
        self.client.force_authenticate(create_user("viewer", "view_cv"))
        response = self.client.post("/api/content/uploads/", {"file": png()})
        self.assertEqual(response.status_code, 403)

    def test_upload_rejects_non_images(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.client.force_authenticate(create_user("editor", "change_cv"))
        upload = SimpleUploadedFile("text.png", b"kein bild", content_type="image/png")
        response = self.client.post("/api/content/uploads/", {"file": upload})
        self.assertEqual(response.status_code, 400)

    def test_upload_stores_image_and_serves_thumbnail(self):
        self.client.force_authenticate(create_user("editor", "change_cv"))
        response = self.client.post("/api/content/uploads/", {"file": png((300, 200))})
        self.assertEqual(response.status_code, 201)
        name = response.data["url"].rsplit("/", 1)[1]
        self.assertRegex(name, r"^[0-9a-f]{32}\.png$")
        thumbnail = self.client.get(f"/api/content/images/{name}/?size=64")
        self.assertEqual(thumbnail["Content-Type"], "image/webp")
        self.assertEqual(
            self.client.get(f"/api/content/images/{name}/?size=65").status_code, 404
        )


class RoleTests(APITestCase):
    def setUp(self):
        self.manager = create_user(
            "manager",
            "view_admin",
            "view_role",
            "add_role",
            "change_role",
            "delete_role",
            "add_permission",
            "delete_permission",
            "view_cv",
        )
        self.client.force_authenticate(self.manager)

    def test_permissions_are_listed_for_admins(self):
        codenames = [
            item["codename"]
            for item in self.client.get("/api/content/permissions/").data
        ]
        self.assertIn("view_cv", codenames)
        self.client.force_authenticate(create_user("guest"))
        self.assertEqual(self.client.get("/api/content/permissions/").status_code, 403)

    def test_role_is_created_with_own_permissions_only(self):
        response = self.client.post(
            "/api/content/roles/",
            {"name": "Leser", "permissions": ["view_cv"]},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["permissions"], ["view_cv"])
        response = self.client.post(
            "/api/content/roles/",
            {"name": "Chef", "permissions": ["change_cv"]},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_role_needs_unique_name(self):
        self.client.post("/api/content/roles/", {"name": "Leser"}, format="json")
        self.assertEqual(
            self.client.post(
                "/api/content/roles/", {"name": "Leser"}, format="json"
            ).status_code,
            400,
        )
        self.assertEqual(
            self.client.post(
                "/api/content/roles/", {"name": " "}, format="json"
            ).status_code,
            400,
        )

    def test_role_is_renamed_updated_and_deleted(self):
        role = self.client.post(
            "/api/content/roles/", {"name": "Leser"}, format="json"
        ).data
        response = self.client.patch(
            f"/api/content/roles/{role['id']}/",
            {"name": "Gäste", "permissions": ["view_cv"]},
            format="json",
        )
        self.assertEqual(
            (response.data["name"], response.data["permissions"]),
            ("Gäste", ["view_cv"]),
        )
        names = [item["name"] for item in self.client.get("/api/content/roles/").data]
        self.assertEqual(names, ["Gäste"])
        self.assertEqual(
            self.client.delete(f"/api/content/roles/{role['id']}/").status_code, 204
        )

    def test_roles_need_view_permission(self):
        self.client.force_authenticate(create_user("guest"))
        self.assertEqual(self.client.get("/api/content/roles/").status_code, 403)
