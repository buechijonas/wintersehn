from rest_framework.permissions import BasePermission

from wintersehn.accounts.consent import consent_of
from wintersehn.accounts.models import get_or_create_profile


class CanViewMonolith(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("content.view_monolith")


class CanViewShared(BasePermission):
    def has_permission(self, request, view):
        verified = get_or_create_profile(request.user).verified
        return verified and all(consent_of(request.user).values())
