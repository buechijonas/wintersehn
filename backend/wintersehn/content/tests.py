from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone
from rest_framework.test import APITestCase

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


def create_user(username, *codenames):
    user = get_user_model().objects.create_user(username)
    user.user_permissions.add(
        *Permission.objects.filter(
            codename__in=codenames, content_type__app_label="content"
        )
    )
    return user


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
                                    {"name": "Brave", "country": "united_states", "footprint": 2}
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
