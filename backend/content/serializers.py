from rest_framework import serializers

from .models import SiteContent
from .validators import validate_links


class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ["key", "data", "updated_at"]
        read_only_fields = ["key", "updated_at"]
        extra_kwargs = {"data": {"validators": [validate_links]}}
