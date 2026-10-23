from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .rbac import MANAGED_PERMISSIONS


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["codename", "name"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def get_permissions(self, obj):
        return list(
            obj.permissions.filter(codename__in=MANAGED_PERMISSIONS).values_list(
                "codename", flat=True
            )
        )
