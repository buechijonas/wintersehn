from unittest.mock import patch

from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase

from commons.testing import create_user

from .models import UserConsent


def role(name, *codenames):
    group = Group.objects.create(name=name)
    group.permissions.set(Permission.objects.filter(codename__in=codenames))
    return group


class MeTests(APITestCase):
    def test_guest_has_no_user(self):
        self.assertIsNone(self.client.get("/api/auth/me/").data["user"])

    def test_user_carries_profile_role_and_flags(self):
        user = create_user("leser", "view_cv")
        user.groups.add(role("Leser", "view_cv"))
        self.client.force_authenticate(user)
        data = self.client.get("/api/auth/me/").data["user"]
        self.assertEqual(
            (data["display_name"], data["role"], data["verified"]),
            ("leser", "Leser", True),
        )
        self.assertTrue(data["can_view_cv"])
        self.assertFalse(data["can_view_admin"])
        self.assertEqual(data["permissions"], ["view_cv"])
        self.assertEqual(
            data["consent"],
            dict.fromkeys(["privacy", "terms", "disclaimer", "cookies"], False),
        )

    def test_logout(self):
        self.client.force_authenticate(create_user("leser"))
        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)


@patch("wintersehn.accounts.views.push_to_govex")
class ConsentTests(APITestCase):
    def setUp(self):
        self.user = create_user("leser")
        self.client.force_authenticate(self.user)

    def test_accepting_a_consent(self, push):
        response = self.client.post("/api/auth/consent/terms/")
        self.assertTrue(response.data["terms"])
        self.assertTrue(UserConsent.objects.get(user=self.user).terms)
        push.assert_called_once()

    def test_unknown_consent_is_missing(self, push):
        self.assertEqual(
            self.client.post("/api/auth/consent/nothing/").status_code, 404
        )


class UserManagementTests(APITestCase):
    def setUp(self):
        self.manager = create_user(
            "chef", "view_role", "assign_user", "change_user", "view_cv"
        )
        self.member = create_user("mitglied")
        self.client.force_authenticate(self.manager)

    def test_users_are_listed_for_role_viewers(self):
        names = [user["username"] for user in self.client.get("/api/auth/users/").data]
        self.assertEqual(names, ["chef", "mitglied"])
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.get("/api/auth/users/").status_code, 403)

    def test_assigning_a_role(self):
        reader = role("Leser", "view_cv")
        response = self.client.patch(
            f"/api/auth/users/{self.member.pk}/role/",
            {"role": reader.pk},
            format="json",
        )
        self.assertEqual(response.data["role"], reader.pk)
        response = self.client.patch(
            f"/api/auth/users/{self.member.pk}/role/", {"role": None}, format="json"
        )
        self.assertIsNone(response.data["role"])

    def test_role_with_foreign_rights_cannot_be_assigned(self):
        boss = role("Chef", "change_cv")
        response = self.client.patch(
            f"/api/auth/users/{self.member.pk}/role/", {"role": boss.pk}, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_member_with_foreign_rights_cannot_be_changed(self):
        self.member.groups.add(role("Chef", "change_cv"))
        response = self.client.patch(
            f"/api/auth/users/{self.member.pk}/role/", {"role": None}, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_own_role_and_verification_stay_unchanged(self):
        for action in ("role", "verify"):
            response = self.client.patch(
                f"/api/auth/users/{self.manager.pk}/{action}/", {}, format="json"
            )
            self.assertEqual(response.status_code, 400)

    def test_verifying_a_user(self):
        response = self.client.patch(
            f"/api/auth/users/{self.member.pk}/verify/",
            {"verified": False},
            format="json",
        )
        self.assertFalse(response.data["verified"])

    def test_assigning_needs_permission(self):
        self.client.force_authenticate(create_user("gast"))
        response = self.client.patch(
            f"/api/auth/users/{self.member.pk}/role/", {"role": None}, format="json"
        )
        self.assertEqual(response.status_code, 403)
