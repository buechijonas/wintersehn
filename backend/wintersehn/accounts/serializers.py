from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from commons.serializers import BaseModelSerializer
from wintersehn.content.rbac import (
    can_grant_permissions,
    permission_flags,
    user_permissions,
)

from .models import CONSENT_FIELDS, UserConsent, get_or_create_profile

User = get_user_model()


class ConsentModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        class Meta(BaseModelSerializer.read.Meta):
            model = UserConsent
            fields = CONSENT_FIELDS


class UserModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        display_name = serializers.SerializerMethodField()
        consent = serializers.SerializerMethodField()
        avatar = serializers.SerializerMethodField()
        birthdate = serializers.SerializerMethodField()
        verified = serializers.SerializerMethodField()
        role = serializers.SerializerMethodField()
        permissions = serializers.SerializerMethodField()

        class Meta(BaseModelSerializer.read.Meta):
            model = User
            fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "display_name",
                "birthdate",
                "consent",
                "avatar",
                "verified",
                "role",
                "permissions",
            ]

        def to_representation(self, user):
            return {**super().to_representation(user), **permission_flags(user)}

        def get_display_name(self, user):
            return user.get_full_name() or user.username

        def get_consent(self, user):
            return UserConsent.of(user).accepted

        def get_avatar(self, user):
            return get_or_create_profile(user).avatar

        def get_birthdate(self, user):
            return get_or_create_profile(user).birthdate

        def get_verified(self, user):
            return get_or_create_profile(user).verified

        def get_role(self, user):
            group = user.groups.first()
            return group.name if group else None

        def get_permissions(self, user):
            return user_permissions(user)

    class list(BaseModelSerializer.read):
        role = serializers.SerializerMethodField()
        avatar = serializers.SerializerMethodField()
        verified = serializers.SerializerMethodField()

        class Meta(BaseModelSerializer.read.Meta):
            model = User
            fields = ["id", "username", "email", "role", "avatar", "verified"]

        def get_role(self, user):
            group = user.groups.first()
            return group.id if group else None

        def get_avatar(self, user):
            return get_or_create_profile(user).avatar

        def get_verified(self, user):
            return get_or_create_profile(user).verified


class RoleAssignmentSerializer(serializers.Serializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), allow_null=True, required=False
    )

    def validate(self, data):
        manager = self.context["request"].user
        member = self.context["member"]
        current = member.groups.values_list("permissions__codename", flat=True)
        if not can_grant_permissions(manager, current):
            raise PermissionDenied(
                "Du kannst die Rolle dieses Nutzers nicht ändern, da sie Rechte enthält, "
                "die du nicht besitzt."
            )
        role = data.get("role")
        if role and not can_grant_permissions(
            manager, role.permissions.values_list("codename", flat=True)
        ):
            raise PermissionDenied(
                "Du kannst nur Rollen zuweisen, deren Rechte du selbst besitzt."
            )
        return data

    def save(self):
        member = self.context["member"]
        role = self.validated_data.get("role")
        member.groups.set([role] if role else [])
        return member


class VerificationSerializer(serializers.Serializer):
    verified = serializers.BooleanField(default=False)

    def save(self):
        profile = get_or_create_profile(self.context["member"])
        profile.verified = self.validated_data["verified"]
        profile.save(update_fields=["verified"])
        return profile.user
