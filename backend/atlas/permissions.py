from rest_framework.permissions import BasePermission


class CanViewAtlas(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("content.view_admin")
