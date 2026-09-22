import io
import uuid

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from PIL import Image
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SiteContent
from .rbac import can_grant_permissions, managed_permissions_queryset, set_role_permissions
from .rbac_serializers import PermissionSerializer, RoleSerializer
from .serializers import SiteContentSerializer

MAX_UPLOAD_SIZE = 512 * 1024 * 1024  # 512 MB
MAX_DIMENSION = 2000
ALLOWED_IMAGE_FORMATS = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "GIF": "gif"}

VIEW_PERMISSION_BY_KEY = {
    "about": "content.view_about",
    "ethos": "content.view_ethos",
    "cv": "content.view_cv",
    "countries": "content.view_countries",
}

CONTENT_CRUD_KEYS = {"about", "ethos", "cv", "countries", "media"}


class SiteContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, key):
        required_perm = VIEW_PERMISSION_BY_KEY.get(key)
        if required_perm and not request.user.has_perm(required_perm):
            return Response(status=status.HTTP_403_FORBIDDEN)

        content = get_object_or_404(SiteContent, key=key)
        data = content.data

        if key == "media" and not request.user.has_perm("content.view_media"):
            data = [group for group in data if not group.get("requiresAuth")]

        return Response(
            {"key": content.key, "data": data, "updated_at": content.updated_at}
        )

    def put(self, request, key):
        if key in CONTENT_CRUD_KEYS:
            allowed = any(
                request.user.has_perm(f"content.{verb}_{key}")
                for verb in ("add", "change", "delete")
            )
        else:
            allowed = request.user.has_perm("content.change_sitecontent")

        if not allowed:
            return Response(status=status.HTTP_403_FORBIDDEN)

        content, _ = SiteContent.objects.get_or_create(key=key, defaults={"data": {}})
        serializer = SiteContentSerializer(
            content, data={"data": request.data.get("data")}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ContentImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        can_write_content = request.user.has_perm(
            "content.change_sitecontent"
        ) or any(
            request.user.has_perm(f"content.{verb}_{key}")
            for key in CONTENT_CRUD_KEYS
            for verb in ("add", "change", "delete")
        )
        if not can_write_content:
            return Response(status=status.HTTP_403_FORBIDDEN)

        upload = request.FILES.get("file")
        if not upload:
            return Response(
                {"detail": "Keine Datei erhalten."}, status=status.HTTP_400_BAD_REQUEST
            )
        if upload.size > MAX_UPLOAD_SIZE:
            return Response(
                {"detail": "Datei ist zu gross (max. 512 MB)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raw = upload.read()
        try:
            Image.open(io.BytesIO(raw)).verify()
            image = Image.open(io.BytesIO(raw))
            image_format = image.format
        except Exception:
            return Response(
                {"detail": "Datei ist kein gültiges Bild."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        extension = ALLOWED_IMAGE_FORMATS.get(image_format)
        if not extension:
            return Response(
                {"detail": "Nicht unterstütztes Bildformat (JPEG, PNG, WEBP, GIF)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if image.width > MAX_DIMENSION or image.height > MAX_DIMENSION:
            if image_format == "JPEG" and image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
            buffer = io.BytesIO()
            image.save(buffer, format=image_format)
            raw = buffer.getvalue()

        saved_path = default_storage.save(
            f"uploads/{uuid.uuid4().hex}.{extension}", ContentFile(raw)
        )
        return Response(
            {"url": f"{settings.MEDIA_URL}{saved_path}"}, status=status.HTTP_201_CREATED
        )


class PermissionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.has_perm("content.view_admin"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        perms = managed_permissions_queryset().order_by("codename")
        return Response(PermissionSerializer(perms, many=True).data)


class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.has_perm("content.view_role"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        groups = Group.objects.all().order_by("name")
        return Response(RoleSerializer(groups, many=True).data)

    def post(self, request):
        if not request.user.has_perm("content.add_role"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        permissions = request.data.get("permissions") or []
        if permissions and not request.user.has_perm("content.add_permission"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not can_grant_permissions(request.user, permissions):
            return Response(
                {"detail": "Du kannst nur Berechtigungen vergeben, die du selbst besitzt."},
                status=status.HTTP_403_FORBIDDEN,
            )

        name = (request.data.get("name") or "").strip()
        if not name:
            return Response(
                {"detail": "Name ist erforderlich."}, status=status.HTTP_400_BAD_REQUEST
            )
        if Group.objects.filter(name=name).exists():
            return Response(
                {"detail": "Diese Rolle existiert bereits."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group = Group.objects.create(name=name)
        set_role_permissions(group, permissions)
        return Response(RoleSerializer(group).data, status=status.HTTP_201_CREATED)


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not request.user.has_perm("content.change_role"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        group = get_object_or_404(Group, pk=pk)
        name = request.data.get("name")
        permissions = request.data.get("permissions")

        if name is not None:
            name = name.strip()
            if not name:
                return Response(
                    {"detail": "Name ist erforderlich."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if permissions is not None:
            current = set(group.permissions.values_list("codename", flat=True))
            desired = set(permissions)
            added = desired - current
            removed = current - desired
            if added and not request.user.has_perm("content.add_permission"):
                return Response(status=status.HTTP_403_FORBIDDEN)
            if removed and not request.user.has_perm("content.delete_permission"):
                return Response(status=status.HTTP_403_FORBIDDEN)
            if not can_grant_permissions(request.user, added):
                return Response(
                    {"detail": "Du kannst nur Berechtigungen vergeben, die du selbst besitzt."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if name is not None:
            group.name = name
            group.save(update_fields=["name"])
        if permissions is not None:
            set_role_permissions(group, permissions)

        return Response(RoleSerializer(group).data)

    def delete(self, request, pk):
        if not request.user.has_perm("content.delete_role"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
