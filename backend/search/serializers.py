import json

from django.core.validators import RegexValidator
from rest_framework import serializers

from commons.serializers import BaseModelSerializer, UUIDModelSerializer

from . import child_protection
from .models import SearchSettings, Sponsor

MAX_SIZE = 20_000
HOST_VALIDATOR = RegexValidator(r"^(?=.{1,253}$)([a-z0-9-]{1,63}\.)+[a-z]{2,63}$")


class SearchSettingsModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        data = serializers.DictField(source="protected_data", read_only=True)

        class Meta(BaseModelSerializer.read.Meta):
            model = SearchSettings
            fields = ["data"]

    class write(BaseModelSerializer.write):
        data = serializers.DictField()

        class Meta(BaseModelSerializer.write.Meta):
            model = SearchSettings
            fields = ["data"]

        def validate_data(self, value):
            if len(json.dumps(value)) > MAX_SIZE:
                raise serializers.ValidationError("Die Einstellungen sind zu gross.")
            return value

        def update(self, instance, validated_data):
            data = child_protection.protect(instance.user, validated_data["data"])
            return super().update(instance, {"data": data})


class SponsorModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        class Meta(UUIDModelSerializer.read.Meta):
            model = Sponsor
            fields = ["uuid", "title", "description", "url"]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = Sponsor
            fields = ["title", "description", "url"]
            extra_kwargs = {
                "title": {"trim_whitespace": True, "allow_blank": False},
                "url": {
                    "error_messages": {"invalid": "Bitte gib eine gültige URL ein."}
                },
            }


class HostRatingsRequestSerializer(serializers.Serializer):
    hosts = serializers.ListField(
        child=serializers.CharField(max_length=253, validators=[HOST_VALIDATOR]),
        max_length=30,
    )
