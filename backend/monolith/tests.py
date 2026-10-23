import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from rest_framework.test import APITestCase

from wintersehn.accounts.models import UserConsent, UserProfile

from .models import Addiction, Dossier, Event, Share, TrustEntry


def create_user(username, govex_sub=None, monolith=False, consent=True):
    user = get_user_model().objects.create_user(username)
    UserProfile.objects.create(user=user, govex_sub=govex_sub, verified=True)
    UserConsent.objects.create(
        user=user, privacy=consent, terms=consent, disclaimer=consent, cookies=consent
    )
    if monolith:
        user.user_permissions.add(
            Permission.objects.get(
                codename="view_monolith", content_type__app_label="content"
            )
        )
    return user


class ShareTests(APITestCase):
    def setUp(self):
        self.owner = create_user("owner", monolith=True)
        self.son = create_user("son", govex_sub="sub-son")
        self.stranger = create_user("stranger", govex_sub="sub-stranger")
        self.father = Dossier.objects.create(title="Vaterakte", ethnicity="Geheimnis")
        self.recipient = Dossier.objects.create(title="Sohnakte", govex_sub="sub-son")
        self.event = Event.objects.create(
            dossier=self.father, title="Streit", date="2026-10-01", text="Geheimtext"
        )
        Addiction.objects.create(
            dossier=self.father, kind="cocaine", frequency="daily", event=self.event
        )
        TrustEntry.objects.create(
            user=self.owner,
            dossier=self.father,
            conduct="lied",
            date="2026-10-02",
            text="Ausrede",
        )
        self.share = Share.objects.create(
            dossier=self.father, recipient=self.recipient, created_by=self.owner
        )
        self.url = f"/api/monolith/shared/{self.share.uuid}/"

    def shared(self, user):
        self.client.force_authenticate(user)
        return self.client.get(self.url)

    def set_rules(self, rules):
        self.client.force_authenticate(self.owner)
        return self.client.put(
            f"/api/monolith/dossiers/{self.father.uuid}/shares/{self.share.uuid}/",
            {"rules": rules},
            format="json",
        )

    def assertHidden(self, response, *secrets):
        body = json.dumps(response.json())
        for secret in secrets:
            self.assertNotIn(secret, body)

    def test_everything_redacted_by_default(self):
        response = self.shared(self.son)
        self.assertEqual(response.status_code, 200)
        self.assertHidden(
            response,
            "Vaterakte",
            "Geheimnis",
            "Streit",
            "Geheimtext",
            "cocaine",
            "lied",
        )
        self.assertEqual(response.json()["title"]["visibility"], "full")

    def test_recipient_without_consent_denied(self):
        UserConsent.objects.filter(user=self.son).update(terms=False)
        self.assertEqual(self.shared(self.son).status_code, 403)

    def test_stranger_gets_404(self):
        self.assertEqual(self.shared(self.stranger).status_code, 404)

    def test_owner_without_govex_link_gets_404(self):
        self.assertEqual(self.shared(self.owner).status_code, 404)

    def test_unlinking_recipient_revokes_access(self):
        self.recipient.govex_sub = None
        self.recipient.save()
        self.assertEqual(self.shared(self.son).status_code, 404)

    def test_value_redaction_keeps_label_only(self):
        self.set_rules({"section:meta": "visible", "field:ethnicity": "value"})
        response = self.shared(self.son)
        self.assertHidden(response, "Geheimnis")
        meta = response.json()["sections"][0]
        self.assertIn("ethnicity", [entry["label"] for entry in meta["items"]])

    def test_item_rule_ignored_while_section_redacted(self):
        self.set_rules({"field:ethnicity": "visible"})
        self.assertHidden(self.shared(self.son), "Geheimnis")

    def test_event_links_respect_linked_item(self):
        self.set_rules(
            {"section:events": "visible", f"event:{self.event.uuid}": "visible"}
        )
        response = self.shared(self.son)
        self.assertIn("Geheimtext", json.dumps(response.json()))
        self.assertHidden(response, "cocaine")

    def test_recipient_cannot_manage_shares(self):
        self.client.force_authenticate(self.son)
        response = self.client.get(f"/api/monolith/dossiers/{self.father.uuid}/shares/")
        self.assertEqual(response.status_code, 403)

    def test_unknown_target_rejected(self):
        self.assertEqual(self.set_rules({"field:secret": "visible"}).status_code, 400)

    def test_recipient_must_be_linked_to_govex(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(
            f"/api/monolith/dossiers/{self.recipient.uuid}/shares/",
            {"recipient": str(self.father.uuid)},
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class ShareLinkTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.owner = create_user("owner", monolith=True)
        self.dossier = Dossier.objects.create(title="Akte", ethnicity="Geheimnis")
        self.link = Share.objects.create(
            dossier=self.dossier, name="Für Mutter", created_by=self.owner
        )

    def open(self, token, password=None, ip="203.0.113.1"):
        data = {} if password is None else {"password": password}
        return self.client.post(
            f"/api/monolith/share/{token}/", data, format="json", HTTP_X_REAL_IP=ip
        )

    def protect(self, password):
        self.link.set_password(password)
        self.link.save()

    def test_open_link_without_account(self):
        response = self.open(self.link.token)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Geheimnis", json.dumps(response.json()))

    def test_password_required(self):
        self.protect("korrekt")
        self.assertEqual(self.open(self.link.token).json(), {"password_required": True})
        self.assertEqual(self.open(self.link.token, "falsch").status_code, 403)
        self.assertEqual(self.open(self.link.token, "korrekt").status_code, 200)

    def test_password_is_hashed(self):
        self.protect("korrekt")
        self.assertNotIn("korrekt", self.link.password)

    def test_govex_share_not_reachable_by_token(self):
        recipient = Dossier.objects.create(title="Empfänger", govex_sub="sub")
        share = Share.objects.create(dossier=self.dossier, recipient=recipient)
        self.assertEqual(self.open(share.token).status_code, 404)

    def test_unknown_token_gets_404(self):
        self.assertEqual(self.open("unbekannt").status_code, 404)

    def test_link_attempts_are_throttled(self):
        self.protect("korrekt")
        statuses = [self.open(self.link.token, "falsch").status_code for _ in range(11)]
        self.assertEqual(statuses[-1], 429)

    def test_link_needs_name(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(
            f"/api/monolith/dossiers/{self.dossier.uuid}/shares/", {}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_link_with_password(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(
            f"/api/monolith/dossiers/{self.dossier.uuid}/shares/",
            {"name": "Für Vater", "password": "geheim123"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["has_password"])
        self.assertNotIn("password", response.json())

    def test_breadcrumbs_censored_by_default(self):
        self.assertEqual(
            self.open(self.link.token).json()["breadcrumbs"],
            {"root": False, "tab": False},
        )

    def test_breadcrumb_levels_configurable(self):
        self.link.set_rules({"breadcrumb:tab": "visible"})
        self.assertEqual(
            self.open(self.link.token).json()["breadcrumbs"],
            {"root": False, "tab": True},
        )

    def test_custom_path(self):
        self.client.force_authenticate(self.owner)
        url = f"/api/monolith/dossiers/{self.dossier.uuid}/shares/{self.link.uuid}/"
        response = self.client.patch(url, {"token": "fuer-mutter"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.open("fuer-mutter").status_code, 200)

    def test_custom_path_validated(self):
        self.client.force_authenticate(self.owner)
        url = f"/api/monolith/dossiers/{self.dossier.uuid}/shares/{self.link.uuid}/"
        other = Share.objects.create(dossier=self.dossier, name="Andere")
        for token in ("kurz", "mit leerzeichen", "../../etc", other.token):
            response = self.client.patch(url, {"token": token}, format="json")
            self.assertEqual(response.status_code, 400, token)

    def test_ip_throttle_uses_real_ip(self):
        self.protect("korrekt")
        for _ in range(10):
            self.open(self.link.token, "falsch", ip="203.0.113.1")
        self.assertEqual(
            self.open(self.link.token, "falsch", ip="203.0.113.1").status_code, 429
        )
        self.assertEqual(
            self.open(self.link.token, "falsch", ip="203.0.113.2").status_code, 403
        )

    def test_forwarded_for_cannot_bypass_ip_throttle(self):
        self.protect("korrekt")
        statuses = [
            self.client.post(
                f"/api/monolith/share/{self.link.token}/",
                {"password": "falsch"},
                format="json",
                HTTP_X_REAL_IP="203.0.113.1",
                HTTP_X_FORWARDED_FOR=f"198.51.100.{index}",
            ).status_code
            for index in range(11)
        ]
        self.assertEqual(statuses[-1], 429)


class DossierListTests(APITestCase):
    def setUp(self):
        self.owner = create_user("owner", monolith=True)
        for title in ("Zoe", "ärni", "Anna", "Bruno"):
            Dossier.objects.create(title=title)
        self.client.force_authenticate(self.owner)

    def titles(self, query=""):
        response = self.client.get("/api/monolith/dossiers/", {"q": query})
        return [dossier["title"] for dossier in response.json()]

    def test_sorted_alphabetically(self):
        self.assertEqual(self.titles(), ["Anna", "ärni", "Bruno", "Zoe"])

    def test_search_filters_case_insensitive(self):
        self.assertEqual(self.titles("BRU"), ["Bruno"])

    def test_points_default_to_zero(self):
        response = self.client.get("/api/monolith/dossiers/")
        self.assertEqual({dossier["points"] for dossier in response.json()}, {0})
