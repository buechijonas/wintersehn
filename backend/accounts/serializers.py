from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserConsent

User = get_user_model()


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsent
        fields = ["privacy", "terms", "disclaimer"]


class UserSerializer(serializers.ModelSerializer):
    consent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "consent"]

    def get_consent(self, obj):
        consent, _ = UserConsent.objects.get_or_create(user=obj)
        return ConsentSerializer(consent).data


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
