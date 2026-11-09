from django.http import HttpResponse
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import catalog, serializers
from .models import MediaFile, Title, Upload, UploadError
from .permissions import CanViewLumon


class LumonViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, CanViewLumon]


def media_types(value):
    if value and value not in catalog.MEDIA_TYPES:
        raise ValidationError({"type": "Unbekannter Typ."})
    return [value] if value else catalog.MEDIA_TYPES


class TitleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    LumonViewSet,
):
    serializer_class = serializers.TitleSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return Title.objects.filter(
            media_type__in=media_types(self.request.query_params.get("type"))
        )


class CatalogViewSet(LumonViewSet):
    @action(detail=False)
    def categories(self, request):
        categories = [
            {"key": key, "label": label} for key, label in catalog.CATEGORIES.items()
        ]
        return Response(serializers.CategorySerializer(categories, many=True).data)

    @action(detail=False)
    def search(self, request):
        category = request.query_params.get("category") or None
        if category and category not in catalog.CATEGORIES:
            raise ValidationError({"category": "Unbekannte Kategorie."})
        results = catalog.search(
            request.query_params.get("q", "").strip(),
            category,
            media_types(request.query_params.get("type")),
            Title.objects.saved(),
        )
        return Response(serializers.ItemSerializer(results, many=True).data)

    @action(detail=False, url_path=r"browse/(?P<media_type>movie|tv)")
    def browse(self, request, media_type):
        library = Title.objects.filter(media_type=media_type)
        overview = catalog.browse(
            media_type,
            serializers.TitleSerializer(library, many=True).data,
            Title.objects.saved(),
        )
        return Response(serializers.BrowseSerializer(overview).data)

    @action(detail=False, url_path=r"tv/(?P<catalog_id>\d+)/seasons/(?P<number>\d+)")
    def season(self, request, catalog_id, number):
        episodes = catalog.season_episodes(int(catalog_id), int(number))
        return Response(serializers.EpisodeSerializer(episodes, many=True).data)

    @action(
        detail=False,
        methods=["post"],
        url_path=r"tv/(?P<catalog_id>\d+)/detect",
    )
    def detect(self, request, catalog_id):
        serializer = serializers.DetectRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        detections = catalog.detect(int(catalog_id), **serializer.validated_data)
        return Response(serializers.DetectionSerializer(detections, many=True).data)

    @action(
        detail=False,
        url_path=r"(?P<media_type>movie|tv)/(?P<catalog_id>\d+)/(?P<kind>poster|backdrop)",
    )
    def artwork(self, request, media_type, catalog_id, kind):
        response = HttpResponse(
            catalog.artwork(media_type, int(catalog_id), kind),
            content_type="image/svg+xml",
        )
        response["Cache-Control"] = "private, max-age=86400"
        return response

    @action(detail=False, url_path=r"(?P<media_type>movie|tv)/(?P<catalog_id>\d+)")
    def show(self, request, media_type, catalog_id):
        result = catalog.detail(media_type, int(catalog_id), Title.objects.saved())
        return Response(serializers.DetailSerializer(result).data)


class MediaViewSet(mixins.RetrieveModelMixin, LumonViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = serializers.PlaybackSerializer
    lookup_field = "uuid"

    @action(detail=True, methods=["post"])
    def progress(self, request, uuid):
        serializer = serializers.ProgressSerializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

    @action(detail=False)
    def auth(self, request):
        return Response(status=204)


class UploadViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, LumonViewSet):
    queryset = Upload.objects.all()
    serializer_class = serializers.UploadSerializer
    lookup_field = "uuid"

    def perform_destroy(self, upload):
        upload.discard()

    @action(detail=True, methods=["put"])
    def chunk(self, request, uuid):
        upload = self.get_object()
        offset = request.query_params.get("offset", "")
        if not offset.isdigit():
            raise ValidationError({"offset": "Position fehlt."})
        try:
            upload.append(request.stream, int(offset))
        except UploadError as error:
            raise ValidationError({"detail": str(error)}) from error
        return Response({"received": upload.received})

    @action(detail=True, methods=["post"])
    def complete(self, request, uuid):
        upload = self.get_object()
        fields = catalog.title_fields(upload.media_type, upload.catalog_id)
        try:
            media = upload.complete(fields)
        except UploadError as error:
            raise ValidationError({"detail": str(error)}) from error
        return Response(serializers.MediaSerializer(media).data)
