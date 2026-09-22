from django.contrib.auth import get_user_model
from rest_framework import serializers

from content.rbac import user_permissions

from .models import AVATAR_CHOICES, UserConsent, get_or_create_profile

User = get_user_model()


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsent
        fields = ["privacy", "terms", "disclaimer"]


class UserSerializer(serializers.ModelSerializer):
    consent = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    verified = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    can_edit_content = serializers.SerializerMethodField()
    can_add_about = serializers.SerializerMethodField()
    can_view_about = serializers.SerializerMethodField()
    can_change_about = serializers.SerializerMethodField()
    can_delete_about = serializers.SerializerMethodField()
    can_add_ethos = serializers.SerializerMethodField()
    can_view_ethos = serializers.SerializerMethodField()
    can_change_ethos = serializers.SerializerMethodField()
    can_delete_ethos = serializers.SerializerMethodField()
    can_add_cv = serializers.SerializerMethodField()
    can_view_cv = serializers.SerializerMethodField()
    can_change_cv = serializers.SerializerMethodField()
    can_delete_cv = serializers.SerializerMethodField()
    can_add_countries = serializers.SerializerMethodField()
    can_view_countries = serializers.SerializerMethodField()
    can_change_countries = serializers.SerializerMethodField()
    can_delete_countries = serializers.SerializerMethodField()
    can_add_media = serializers.SerializerMethodField()
    can_view_media = serializers.SerializerMethodField()
    can_change_media = serializers.SerializerMethodField()
    can_delete_media = serializers.SerializerMethodField()
    can_view_admin = serializers.SerializerMethodField()
    can_add_permission = serializers.SerializerMethodField()
    can_delete_permission = serializers.SerializerMethodField()
    can_add_role = serializers.SerializerMethodField()
    can_change_role = serializers.SerializerMethodField()
    can_view_role = serializers.SerializerMethodField()
    can_delete_role = serializers.SerializerMethodField()
    can_change_user = serializers.SerializerMethodField()
    can_assign_user = serializers.SerializerMethodField()
    can_delete_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "consent",
            "avatar",
            "verified",
            "role",
            "permissions",
            "can_edit_content",
            "can_add_about",
            "can_view_about",
            "can_change_about",
            "can_delete_about",
            "can_add_ethos",
            "can_view_ethos",
            "can_change_ethos",
            "can_delete_ethos",
            "can_add_cv",
            "can_view_cv",
            "can_change_cv",
            "can_delete_cv",
            "can_add_countries",
            "can_view_countries",
            "can_change_countries",
            "can_delete_countries",
            "can_add_media",
            "can_view_media",
            "can_change_media",
            "can_delete_media",
            "can_view_admin",
            "can_add_permission",
            "can_delete_permission",
            "can_add_role",
            "can_change_role",
            "can_view_role",
            "can_delete_role",
            "can_change_user",
            "can_assign_user",
            "can_delete_user",
        ]

    def get_consent(self, obj):
        consent, _ = UserConsent.objects.get_or_create(user=obj)
        return ConsentSerializer(consent).data

    def get_avatar(self, obj):
        return get_or_create_profile(obj).avatar

    def get_verified(self, obj):
        return get_or_create_profile(obj).verified

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None

    def get_permissions(self, obj):
        return user_permissions(obj)

    def get_can_edit_content(self, obj):
        return obj.has_perm("content.change_sitecontent")

    def get_can_add_about(self, obj):
        return obj.has_perm("content.add_about")

    def get_can_view_about(self, obj):
        return obj.has_perm("content.view_about")

    def get_can_change_about(self, obj):
        return obj.has_perm("content.change_about")

    def get_can_delete_about(self, obj):
        return obj.has_perm("content.delete_about")

    def get_can_add_ethos(self, obj):
        return obj.has_perm("content.add_ethos")

    def get_can_view_ethos(self, obj):
        return obj.has_perm("content.view_ethos")

    def get_can_change_ethos(self, obj):
        return obj.has_perm("content.change_ethos")

    def get_can_delete_ethos(self, obj):
        return obj.has_perm("content.delete_ethos")

    def get_can_add_cv(self, obj):
        return obj.has_perm("content.add_cv")

    def get_can_view_cv(self, obj):
        return obj.has_perm("content.view_cv")

    def get_can_change_cv(self, obj):
        return obj.has_perm("content.change_cv")

    def get_can_delete_cv(self, obj):
        return obj.has_perm("content.delete_cv")

    def get_can_add_countries(self, obj):
        return obj.has_perm("content.add_countries")

    def get_can_view_countries(self, obj):
        return obj.has_perm("content.view_countries")

    def get_can_change_countries(self, obj):
        return obj.has_perm("content.change_countries")

    def get_can_delete_countries(self, obj):
        return obj.has_perm("content.delete_countries")

    def get_can_add_media(self, obj):
        return obj.has_perm("content.add_media")

    def get_can_view_media(self, obj):
        return obj.has_perm("content.view_media")

    def get_can_change_media(self, obj):
        return obj.has_perm("content.change_media")

    def get_can_delete_media(self, obj):
        return obj.has_perm("content.delete_media")

    def get_can_view_admin(self, obj):
        return obj.has_perm("content.view_admin")

    def get_can_add_permission(self, obj):
        return obj.has_perm("content.add_permission")

    def get_can_delete_permission(self, obj):
        return obj.has_perm("content.delete_permission")

    def get_can_add_role(self, obj):
        return obj.has_perm("content.add_role")

    def get_can_change_role(self, obj):
        return obj.has_perm("content.change_role")

    def get_can_view_role(self, obj):
        return obj.has_perm("content.view_role")

    def get_can_delete_role(self, obj):
        return obj.has_perm("content.delete_role")

    def get_can_change_user(self, obj):
        return obj.has_perm("content.change_user")

    def get_can_assign_user(self, obj):
        return obj.has_perm("content.assign_user")

    def get_can_delete_user(self, obj):
        return obj.has_perm("content.delete_user")


class UserRoleSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "avatar", "verified"]

    def get_role(self, obj):
        group = obj.groups.first()
        return group.id if group else None

    def get_avatar(self, obj):
        return get_or_create_profile(obj).avatar

    def get_verified(self, obj):
        return get_or_create_profile(obj).verified


class ProfileUpdateSerializer(serializers.Serializer):
    # Username and email are owned by govex and re-synced on every login.
    avatar = serializers.ChoiceField(choices=AVATAR_CHOICES, required=False, allow_blank=True)

    def save(self):
        user = self.instance
        if "avatar" in self.validated_data:
            profile = get_or_create_profile(user)
            profile.avatar = self.validated_data["avatar"]
            profile.save(update_fields=["avatar"])
        return user
