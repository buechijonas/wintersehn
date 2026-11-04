import json

from rest_framework import serializers

from .models import SearchSettings, Sponsor

MAX_SIZE = 20_000


class SearchSettingsSerializer(serializers.ModelSerializer):
    data = serializers.DictField()

    class Meta:
        model = SearchSettings
        fields = ["data"]

    def validate_data(self, value):
        if len(json.dumps(value)) > MAX_SIZE:
            raise serializers.ValidationError("Die Einstellungen sind zu gross.")
        return value


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ["uuid", "title", "description", "url"]
        extra_kwargs = {
            "title": {"trim_whitespace": True, "allow_blank": False},
            "url": {"error_messages": {"invalid": "Bitte gib eine gültige URL ein."}},
        }
