from datetime import date
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase

from wintersehn.accounts.models import UserProfile

from .child_protection import DOMAINS, age
from .lookalike import check
from .models import SearchSettings


def create_user(username, birthdate):
    user = get_user_model().objects.create_user(username)
    UserProfile.objects.create(user=user, birthdate=birthdate, verified=True)
    return user


def years_ago(years):
    today = date.today()
    return today.replace(year=today.year - years, day=1)


class LookalikeTests(APITestCase):
    def test_plain_host_is_not_flagged(self):
        self.assertIsNone(check("apple.com"))

    def test_latin_umlaut_is_not_flagged(self):
        self.assertIsNone(check("xn--zrich-kva.ch"))

    def test_cyrillic_lookalike_is_flagged(self):
        self.assertEqual(
            check("xn--pple-43d.com"), {"lookalike": True, "unicode": "аpple.com"}
        )

    def test_cyrillic_only_lookalike_is_flagged(self):
        self.assertTrue(check("xn--80ak6aa92e.com")["lookalike"])

    def test_broken_punycode_is_flagged(self):
        self.assertTrue(check("xn--99999.com")["lookalike"])


class HostRatingsTests(APITestCase):
    def setUp(self):
        cache.clear()

    @mock.patch("search.observatory.fetch_report", return_value={})
    def test_returns_lookalikes_without_observatory_grade(self, fetch_report):
        response = self.client.post(
            "/api/search/host-ratings/",
            {"hosts": ["xn--pple-43d.com", "example.com"]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["hosts"],
            {"xn--pple-43d.com": {"lookalike": True, "unicode": "аpple.com"}},
        )


class ChildProtectionTests(APITestCase):
    def test_age_counts_birthday(self):
        self.assertEqual(age(date(2008, 11, 6), date(2026, 11, 5)), 17)
        self.assertEqual(age(date(2008, 11, 5), date(2026, 11, 5)), 18)

    def test_guest_is_not_protected(self):
        response = self.client.get("/api/search/child-protection/")
        self.assertFalse(response.json()["required"])
        self.assertEqual(response.json()["domains"], DOMAINS)

    def test_minor_is_protected(self):
        self.client.force_authenticate(create_user("kid", years_ago(17)))
        response = self.client.get("/api/search/child-protection/")
        self.assertTrue(response.json()["required"])

    def test_adult_and_unknown_birthdate_are_not_protected(self):
        for username, birthdate in [("adult", years_ago(19)), ("unknown", None)]:
            self.client.force_authenticate(create_user(username, birthdate))
            response = self.client.get("/api/search/child-protection/")
            self.assertFalse(response.json()["required"])

    def test_minor_cannot_change_allowlist(self):
        self.client.force_authenticate(create_user("kid", years_ago(12)))
        data = {
            "allowlist": ["example.com"],
            "allowlistEnabled": False,
            "language": "en",
        }
        response = self.client.put(
            "/api/search/settings/", {"data": data}, format="json"
        )
        saved = response.json()["data"]
        self.assertEqual(saved["allowlist"], DOMAINS)
        self.assertTrue(saved["allowlistEnabled"])
        self.assertEqual(saved["language"], "en")

    def test_minor_gets_protected_settings(self):
        user = create_user("kid", years_ago(12))
        SearchSettings.objects.create(user=user, data={"allowlistEnabled": False})
        self.client.force_authenticate(user)
        saved = self.client.get("/api/search/settings/").json()["data"]
        self.assertEqual(saved["allowlist"], DOMAINS)
        self.assertTrue(saved["allowlistEnabled"])

    def test_adult_can_change_allowlist(self):
        self.client.force_authenticate(create_user("adult", years_ago(30)))
        data = {"allowlist": [], "allowlistEnabled": False}
        response = self.client.put(
            "/api/search/settings/", {"data": data}, format="json"
        )
        self.assertEqual(response.json()["data"], data)
