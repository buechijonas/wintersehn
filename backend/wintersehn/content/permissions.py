from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import SiteContent


class SiteContentPermission(BasePermission):
    def has_object_permission(self, request, view, content):
        if request.method in SAFE_METHODS:
            return SiteContent.can_view(request.user, content.key)
        return SiteContent.can_edit(request.user, content.key)


class UploadPermission(BasePermission):
    def has_permission(self, request, view):
        return SiteContent.can_upload(request.user)


class CountriesPermission(BasePermission):
    def has_permission(self, request, view):
        verb = "view" if request.method in SAFE_METHODS else "change"
        return request.user.has_perm(f"content.{verb}_countries")
