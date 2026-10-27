from rest_framework.permissions import SAFE_METHODS, BasePermission


class CountriesPermission(BasePermission):
    def has_permission(self, request, view):
        verb = "view" if request.method in SAFE_METHODS else "change"
        return request.user.has_perm(f"content.{verb}_countries")
