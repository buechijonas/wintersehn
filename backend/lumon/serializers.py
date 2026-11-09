from rest_framework import serializers

from commons.serializers import UUIDModelSerializer

from . import catalog
from .models import MediaFile, Title, Upload


class TitleModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        saved = serializers.UUIDField(source="uuid", read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Title
            fields = [
                "uuid",
                "catalog_id",
                "media_type",
                "title",
                "year",
                "poster",
                "saved",
            ]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = Title
            fields = ["catalog_id", "media_type"]

        def create(self, validated_data):
            fields = catalog.title_fields(
                validated_data["media_type"], validated_data["catalog_id"]
            )
            return super().create({**validated_data, **fields})


class ItemSerializer(serializers.Serializer):
    catalog_id = serializers.IntegerField()
    media_type = serializers.CharField()
    title = serializers.CharField()
    year = serializers.IntegerField(allow_null=True)
    poster = serializers.CharField(allow_null=True)
    saved = serializers.UUIDField(allow_null=True)


class RowSerializer(serializers.Serializer):
    key = serializers.CharField()
    title = serializers.CharField()
    items = ItemSerializer(many=True)


class ChannelSerializer(serializers.Serializer):
    name = serializers.CharField()
    link = serializers.CharField(allow_null=True)


class MediaFileModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        id = serializers.UUIDField(source="uuid", read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = MediaFile
            fields = ["id", "played", "position", "duration", "subtitle"]

    class retrieve(read):
        next = serializers.UUIDField(
            source="following.uuid", allow_null=True, read_only=True
        )

        class Meta(UUIDModelSerializer.read.Meta):
            model = MediaFile
            fields = [
                "id",
                "played",
                "position",
                "duration",
                "subtitle",
                "title",
                "next",
                "stream",
            ]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = MediaFile
            fields = ["played", "position", "duration"]


class SeasonSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    name = serializers.CharField()
    episodes = serializers.IntegerField()


class EpisodeSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField(allow_blank=True)
    still = serializers.CharField(allow_null=True)
    runtime = serializers.IntegerField(allow_null=True)
    air_date = serializers.CharField(allow_null=True)
    media = MediaFileModelSerializer.read(allow_null=True)


class DetectRequestSerializer(serializers.Serializer):
    filenames = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    default_season = serializers.IntegerField(min_value=1, default=1)


class DetectionSerializer(serializers.Serializer):
    filename = serializers.CharField()
    season = serializers.IntegerField(allow_null=True)
    episode = serializers.IntegerField(allow_null=True)
    title = serializers.CharField(allow_null=True)
    exists = serializers.BooleanField()


class DetailSerializer(ItemSerializer):
    overview = serializers.CharField(allow_blank=True)
    backdrop = serializers.CharField(allow_null=True)
    genres = serializers.ListField(child=serializers.CharField())
    rating = serializers.FloatField(allow_null=True)
    runtime = serializers.IntegerField(allow_null=True)
    seasons = SeasonSerializer(many=True)
    channel = ChannelSerializer(allow_null=True)
    media = MediaFileModelSerializer.read(allow_null=True)


class CategorySerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()


class UploadModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        class Meta(UUIDModelSerializer.read.Meta):
            model = Upload
            fields = [
                "uuid",
                "media_type",
                "catalog_id",
                "season",
                "episode",
                "size",
                "received",
            ]

    class write(UUIDModelSerializer.write):
        filename = serializers.CharField(write_only=True)

        class Meta(UUIDModelSerializer.write.Meta):
            model = Upload
            fields = [
                "media_type",
                "catalog_id",
                "season",
                "episode",
                "filename",
                "size",
            ]

        def validate(self, data):
            extension = data.pop("filename").rsplit(".", 1)[-1].lower()
            if extension not in Upload.EXTENSIONS:
                raise serializers.ValidationError(
                    {"filename": f"Erlaubt sind {', '.join(Upload.EXTENSIONS)}."}
                )
            if data["media_type"] == Title.TV and not (
                data.get("season") and data.get("episode")
            ):
                raise serializers.ValidationError(
                    {"episode": "Staffel und Folge fehlen."}
                )
            if data["media_type"] == Title.MOVIE:
                data.update(season=None, episode=None)
            return {**data, "extension": extension}


class BrowseSerializer(serializers.Serializer):
    featured = DetailSerializer(allow_null=True)
    rows = RowSerializer(many=True)
