from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("content.view_admin")


class ActionPermission(BasePermission):
    def has_permission(self, request, view):
        permission = view.action_permissions.get(view.action)
        return permission is None or request.user.has_perm(permission)
