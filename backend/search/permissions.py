from rest_framework.permissions import SAFE_METHODS, BasePermission


class SponsorsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.has_perm("content.view_admin")
