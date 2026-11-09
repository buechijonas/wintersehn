from rest_framework import serializers

from commons.serializers import BaseModelSerializer

from .countries import COUNTRY_CODES, COUNTRY_POINTS
from .models import Destination, SiteContent
from .validators import validate_links


class SiteContentModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        data = serializers.SerializerMethodField()

        class Meta(BaseModelSerializer.read.Meta):
            model = SiteContent
            fields = ["key", "data", "updated_at"]

        def get_data(self, content):
            return content.visible_data(self.context["request"].user)

    class write(BaseModelSerializer.write):
        class Meta(BaseModelSerializer.write.Meta):
            model = SiteContent
            fields = ["data"]
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


class DestinationModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        label = serializers.CharField(source="country.label", read_only=True)
        section = serializers.IntegerField(source="country.section", read_only=True)
        item = serializers.IntegerField(source="country.item", read_only=True)
        days_left = serializers.IntegerField(read_only=True)

        class Meta(BaseModelSerializer.read.Meta):
            model = Destination
            fields = ["icon", "date", "label", "section", "item", "days_left"]

    class write(BaseModelSerializer.write):
        class Meta(BaseModelSerializer.write.Meta):
            model = Destination
            fields = ["icon", "date"]

        def validate_icon(self, icon):
            if not Destination(icon=icon).country:
                raise serializers.ValidationError("Dieses Land ist in keiner Liste.")
            return icon


class CountryMapSerializer(serializers.Serializer):
    destination = DestinationModelSerializer.read(allow_null=True)
    sections = CountrySectionSerializer(many=True)


class FootprintCountrySerializer(serializers.Serializer):
    label = serializers.CharField()
    icon = serializers.CharField(allow_null=True)
    value = serializers.IntegerField()
    share = serializers.IntegerField()
    weight = serializers.FloatField()
    code = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()

    def get_code(self, item):
        return COUNTRY_CODES.get(item["icon"])

    def get_point(self, item):
        return COUNTRY_POINTS.get(item["icon"])


class FootprintRegionSerializer(serializers.Serializer):
    label = serializers.CharField()
    icon = serializers.CharField(allow_null=True)
    value = serializers.IntegerField()
    share = serializers.IntegerField()


class FootprintSummarySerializer(serializers.Serializer):
    value = serializers.IntegerField()
    max = serializers.IntegerField()
    countries = FootprintCountrySerializer(many=True)
    regions = FootprintRegionSerializer(many=True)


class FootprintSerializer(serializers.Serializer):
    before = FootprintSummarySerializer()
    after = FootprintSummarySerializer()
    reduction = serializers.IntegerField()
    flags = serializers.DictField(child=serializers.CharField())


class NowSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()


class StatSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.IntegerField(allow_null=True)
    unit = serializers.CharField()


class RetrospectSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(default="")
    year = serializers.CharField()
    years_ago = serializers.IntegerField()
    section = serializers.CharField()


class ReplacedSerializer(serializers.Serializer):
    name = serializers.CharField()
    icon = serializers.CharField(default=None)


class MediumSerializer(serializers.Serializer):
    name = serializers.CharField()
    icon = serializers.CharField(default=None)
    url = serializers.CharField(default=None)
    category = serializers.CharField(default="")
    reason = serializers.CharField(default="")


class AlternativeSerializer(MediumSerializer):
    replaces = ReplacedSerializer(many=True)


class DashboardSerializer(serializers.Serializer):
    now = NowSerializer(many=True)
    stats = StatSerializer(many=True)
    retrospect = RetrospectSerializer(allow_null=True)
    alternative = AlternativeSerializer(allow_null=True)
    medium = MediumSerializer(allow_null=True)
