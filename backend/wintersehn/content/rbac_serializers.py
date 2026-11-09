from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from commons.serializers import BaseModelSerializer

from .rbac import MANAGED_PERMISSIONS, can_grant_permissions, set_role_permissions


class PermissionModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        class Meta(BaseModelSerializer.read.Meta):
            model = Permission
            fields = ["codename", "name"]


class RoleModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        permissions = serializers.SerializerMethodField()

        class Meta(BaseModelSerializer.read.Meta):
            model = Group
            fields = ["id", "name", "permissions"]

        def get_permissions(self, group):
            return list(
                group.permissions.filter(codename__in=MANAGED_PERMISSIONS).values_list(
                    "codename", flat=True
                )
            )

    class write(BaseModelSerializer.write):
        name = serializers.CharField(
            trim_whitespace=True, allow_blank=False, required=False
        )
        permissions = serializers.ListField(
            child=serializers.CharField(), required=False
        )

        class Meta(BaseModelSerializer.write.Meta):
            model = Group
            fields = ["name", "permissions"]

        def validate_name(self, name):
            taken = Group.objects.filter(name=name)
            if self.instance:
                taken = taken.exclude(pk=self.instance.pk)
            if taken.exists():
                raise serializers.ValidationError("Diese Rolle existiert bereits.")
            return name

        def validate(self, data):
            if not self.instance and "name" not in data:
                raise serializers.ValidationError({"name": "Name ist erforderlich."})
            if "permissions" in data:
                self.check_grants(set(data["permissions"]))
            return data

        def check_grants(self, desired):
            user = self.context["request"].user
            current = set()
            if self.instance:
                current = set(
                    self.instance.permissions.values_list("codename", flat=True)
                )
            if desired - current and not user.has_perm("content.add_permission"):
                raise PermissionDenied()
            if current - desired and not user.has_perm("content.delete_permission"):
                raise PermissionDenied()
            if not can_grant_permissions(user, desired - current):
                raise PermissionDenied(
                    "Du kannst nur Berechtigungen vergeben, die du selbst besitzt."
                )

        def create(self, validated_data):
            group = Group.objects.create(name=validated_data["name"])
            set_role_permissions(group, validated_data.get("permissions", []))
            return group

        def update(self, group, validated_data):
            if "name" in validated_data:
                group.name = validated_data["name"]
                group.save(update_fields=["name"])
            if "permissions" in validated_data:
                set_role_permissions(group, validated_data["permissions"])
            return group
