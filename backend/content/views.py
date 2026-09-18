from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SiteContent
from .rbac import managed_permissions_queryset, set_role_permissions
from .rbac_serializers import PermissionSerializer, RoleSerializer
from .serializers import SiteContentSerializer

VIEW_PERMISSION_BY_KEY = {
    "about": "content.view_about",
    "ethos": "content.view_ethos",
    "cv": "content.view_cv",
    "countries": "content.view_countries",
    "media": "content.view_media",
}


class SiteContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, key):
        required_perm = VIEW_PERMISSION_BY_KEY.get(key)
        if required_perm and not request.user.has_perm(required_perm):
            return Response(status=status.HTTP_403_FORBIDDEN)

        content = get_object_or_404(SiteContent, key=key)
        return Response(SiteContentSerializer(content).data)

    def put(self, request, key):
        if not request.user.has_perm("content.change_sitecontent"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        content, _ = SiteContent.objects.get_or_create(key=key, defaults={"data": {}})
        serializer = SiteContentSerializer(
            content, data={"data": request.data.get("data")}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
        if not request.user.has_perm("content.view_admin"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        groups = Group.objects.all().order_by("name")
        return Response(RoleSerializer(groups, many=True).data)

    def post(self, request):
        if not request.user.has_perm("content.manage_roles"):
            return Response(status=status.HTTP_403_FORBIDDEN)

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
        set_role_permissions(group, request.data.get("permissions", []))
        return Response(RoleSerializer(group).data, status=status.HTTP_201_CREATED)


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        name = request.data.get("name")
        permissions = request.data.get("permissions")

        if name is not None:
            if not request.user.has_perm("content.manage_roles"):
                return Response(status=status.HTTP_403_FORBIDDEN)
            name = name.strip()
            if not name:
                return Response(
                    {"detail": "Name ist erforderlich."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            group.name = name
            group.save(update_fields=["name"])

        if permissions is not None:
            if not request.user.has_perm("content.manage_permissions"):
                return Response(status=status.HTTP_403_FORBIDDEN)
            set_role_permissions(group, permissions)

        return Response(RoleSerializer(group).data)

    def delete(self, request, pk):
        if not request.user.has_perm("content.manage_roles"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
