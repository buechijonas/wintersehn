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
