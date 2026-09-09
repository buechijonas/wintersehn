from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import SiteContent

MANAGED_PERMISSIONS = [
    "view_about",
    "view_ethos",
    "view_cv",
    "view_countries",
    "view_media",
    "view_admin",
    "change_sitecontent",
    "manage_permissions",
    "manage_roles",
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
