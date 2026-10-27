from rest_framework import serializers

from .countries import COUNTRY_CODES, COUNTRY_POINTS
from .models import Destination, SiteContent
from .validators import validate_links


class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ["key", "data", "updated_at"]
        read_only_fields = ["key", "updated_at"]
        extra_kwargs = {"data": {"validators": [validate_links]}}


class CountrySerializer(serializers.Serializer):
    label = serializers.CharField()
    icon = serializers.CharField()
    code = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()

    def get_code(self, item):
        return COUNTRY_CODES.get(item["icon"])

    def get_point(self, item):
        return COUNTRY_POINTS.get(item["icon"])


class CountrySectionSerializer(serializers.Serializer):
    title = serializers.CharField()
    countries = CountrySerializer(many=True, source="items")


class DestinationSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="country.label", read_only=True)
    section = serializers.IntegerField(source="country.section", read_only=True)
    item = serializers.IntegerField(source="country.item", read_only=True)
    days_left = serializers.IntegerField(read_only=True)

    class Meta:
        model = Destination
        fields = ["icon", "date", "label", "section", "item", "days_left"]

    def validate_icon(self, icon):
        if not Destination(icon=icon).country:
            raise serializers.ValidationError("Dieses Land ist in keiner Liste.")
        return icon


class CountryMapSerializer(serializers.Serializer):
    destination = DestinationSerializer(allow_null=True)
    sections = CountrySectionSerializer(many=True)
