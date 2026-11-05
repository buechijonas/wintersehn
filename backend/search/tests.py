from unittest import mock

from django.core.cache import cache
from rest_framework.test import APITestCase

from .lookalike import check


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
