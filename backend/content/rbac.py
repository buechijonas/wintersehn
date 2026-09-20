from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import SiteContent

CONTENT_CRUD_KEYS = ["about", "ethos", "cv", "countries", "media"]

MANAGED_PERMISSIONS = [
    "view_admin",
    "change_sitecontent",
    *[f"{verb}_{key}" for key in CONTENT_CRUD_KEYS for verb in ("add", "view", "change", "delete")],
    "add_permission",
    "change_permission",
    "delete_permission",
    "add_role",
    "change_role",
    "view_role",
    "delete_role",
]


def managed_permissions_queryset():
    content_type = ContentType.objects.get_for_model(SiteContent)
    return Permission.objects.filter(
        content_type=content_type, codename__in=MANAGED_PERMISSIONS
    )


def set_role_permissions(group, codenames):
    valid_codenames = set(codenames) & set(MANAGED_PERMISSIONS)
    group.permissions.set(
        managed_permissions_queryset().filter(codename__in=valid_codenames)
    )
