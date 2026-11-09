from django.contrib.auth.models import Group
from django.http import FileResponse, Http404
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from commons.permissions import ActionPermission, IsAdmin
from commons.views import BaseViewSet, CreateModelMixin, UpdateModelMixin

from . import images
from .dashboard import dashboard
from .footprint import footprint, privacy_section
from .models import Destination, SiteContent
from .permissions import (
    CountriesPermission,
    SiteContentPermission,
    UploadPermission,
)
from .rbac import managed_permissions_queryset
from .rbac_serializers import PermissionModelSerializer, RoleModelSerializer
from .serializers import (
    CountryMapSerializer,
    DashboardSerializer,
    DestinationModelSerializer,
    FootprintSerializer,
    SiteContentModelSerializer,
)


class SiteContentViewSet(mixins.RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    serializer_class = SiteContentModelSerializer
    permission_classes = [SiteContentPermission]
    lookup_field = "key"

    def get_queryset(self):
        return SiteContent.objects.all()

    def get_object(self):
        key = self.kwargs["key"]
        content = self.get_queryset().filter(key=key).first()
        if not content and self.action != "update":
            raise Http404
        content = content or SiteContent(key=key, data={})
        self.check_object_permissions(self.request, content)
        return content


class CountryMapViewSet(BaseViewSet):
    permission_classes = [CountriesPermission]

    def list(self, request):
        country_map = {
            "destination": Destination.objects.current(),
            "sections": SiteContent.objects.data("countries", []),
        }
        return Response(CountryMapSerializer(country_map).data)


class DestinationViewSet(CountryMapViewSet):
    def update(self, request):
        serializer = DestinationModelSerializer.write(
            Destination.objects.first(), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.list(request)

    def destroy(self, request):
        Destination.objects.all().delete()
        return self.list(request)


class FootprintViewSet(BaseViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        section = privacy_section(SiteContent.objects.data("news", []))
        if not section:
            raise Http404
        return Response(FootprintSerializer(footprint(section)).data)


class DashboardViewSet(BaseViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        return Response(DashboardSerializer(dashboard(request.user)).data)


class UploadViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, UploadPermission]
    parser_classes = [MultiPartParser]

    def create(self, request):
        upload = request.FILES.get("file")
        if not upload:
            raise ValidationError({"detail": "Keine Datei erhalten."})
        return Response({"url": images.store(upload)}, status=201)


class ImageViewSet(BaseViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, name):
        size = request.query_params.get("size", "")
        target = images.thumbnail(name, int(size)) if size.isdigit() else None
        if not target:
            raise Http404
        response = FileResponse(target.open("rb"), content_type="image/webp")
        response["Cache-Control"] = "public, max-age=31536000, immutable"
        return response


class PermissionViewSet(mixins.ListModelMixin, BaseViewSet):
    serializer_class = PermissionModelSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = None

    def get_queryset(self):
        return managed_permissions_queryset().order_by("codename")


class RoleViewSet(
    mixins.ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    serializer_class = RoleModelSerializer
    permission_classes = [IsAuthenticated, ActionPermission]
    action_permissions = {
        "list": "content.view_role",
        "create": "content.add_role",
        "partial_update": "content.change_role",
        "destroy": "content.delete_role",
    }
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = None

    def get_queryset(self):
        return Group.objects.order_by("name")
