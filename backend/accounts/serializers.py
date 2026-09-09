from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

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
    can_edit_content = serializers.SerializerMethodField()
    can_view_about = serializers.SerializerMethodField()
    can_view_ethos = serializers.SerializerMethodField()
    can_view_cv = serializers.SerializerMethodField()
    can_view_countries = serializers.SerializerMethodField()
    can_view_media = serializers.SerializerMethodField()
    can_view_admin = serializers.SerializerMethodField()
    can_manage_permissions = serializers.SerializerMethodField()
    can_manage_roles = serializers.SerializerMethodField()

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
            "can_edit_content",
            "can_view_about",
            "can_view_ethos",
            "can_view_cv",
            "can_view_countries",
            "can_view_media",
            "can_view_admin",
            "can_manage_permissions",
            "can_manage_roles",
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

    def get_can_edit_content(self, obj):
        return obj.has_perm("content.change_sitecontent")

    def get_can_view_about(self, obj):
        return obj.has_perm("content.view_about")

    def get_can_view_ethos(self, obj):
        return obj.has_perm("content.view_ethos")

    def get_can_view_cv(self, obj):
        return obj.has_perm("content.view_cv")

    def get_can_view_countries(self, obj):
        return obj.has_perm("content.view_countries")

    def get_can_view_media(self, obj):
        return obj.has_perm("content.view_media")

    def get_can_view_admin(self, obj):
        return obj.has_perm("content.view_admin")

    def get_can_manage_permissions(self, obj):
        return obj.has_perm("content.manage_permissions")

    def get_can_manage_roles(self, obj):
        return obj.has_perm("content.manage_roles")


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


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Dieser Benutzername ist bereits vergeben."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    avatar = serializers.ChoiceField(choices=AVATAR_CHOICES, required=False, allow_blank=True)

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Benutzername darf nicht leer sein.")
        if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
            raise serializers.ValidationError("Dieser Benutzername ist bereits vergeben.")
        return value

    def save(self):
        user = self.instance
        if "username" in self.validated_data:
            user.username = self.validated_data["username"]
        if "email" in self.validated_data:
            user.email = self.validated_data["email"]
        user.save()

        if "avatar" in self.validated_data:
            profile = get_or_create_profile(user)
            profile.avatar = self.validated_data["avatar"]
            profile.save(update_fields=["avatar"])
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_current_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError("Aktuelles Passwort ist falsch.")
        return value

    def save(self):
        user = self.instance
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
