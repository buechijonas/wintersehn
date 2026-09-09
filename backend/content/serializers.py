from rest_framework import serializers

from .models import SiteContent


class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ["key", "data", "updated_at"]
        read_only_fields = ["key", "updated_at"]
