from django.contrib.auth import get_user_model, logout
from django.contrib.auth.models import Group
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from content.rbac import can_grant_permissions

from .models import UserConsent, get_or_create_profile
from .serializers import (
    ConsentSerializer,
    ProfileUpdateSerializer,
    UserRoleSerializer,
    UserSerializer,
)

CONSENT_FIELDS = {"privacy", "terms", "disclaimer"}
User = get_user_model()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsentAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, field):
        if field not in CONSENT_FIELDS:
            return Response(status=status.HTTP_404_NOT_FOUND)
        consent, _ = UserConsent.objects.get_or_create(user=request.user)
        setattr(consent, field, True)
        consent.save(update_fields=[field])
        return Response(ConsentSerializer(consent).data)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.has_perm("content.view_role"):
            return Response(status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all().order_by("username")
        return Response(UserRoleSerializer(users, many=True).data)


class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not request.user.has_perm("content.assign_user"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if int(pk) == request.user.pk:
            return Response(
                {"detail": "Du kannst deine eigene Rolle nicht ändern."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=pk)
        current_permissions = user.groups.values_list("permissions__codename", flat=True)
        if not can_grant_permissions(request.user, current_permissions):
            return Response(
                {"detail": "Du kannst die Rolle dieses Nutzers nicht ändern, da sie Rechte enthält, die du nicht besitzt."},
                status=status.HTTP_403_FORBIDDEN,
            )

        role_id = request.data.get("role")
        if role_id:
            group = get_object_or_404(Group, pk=role_id)
            role_permissions = group.permissions.values_list("codename", flat=True)
            if not can_grant_permissions(request.user, role_permissions):
                return Response(
                    {"detail": "Du kannst nur Rollen zuweisen, deren Rechte du selbst besitzt."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            user.groups.set([group])
        else:
            user.groups.clear()
        return Response(UserRoleSerializer(user).data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Deleting your own account never requires a permission.
        is_self = int(pk) == request.user.pk
        if not is_self and not request.user.has_perm("content.delete_user"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, pk=pk)
        if is_self:
            logout(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not request.user.has_perm("content.change_user"):
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, pk=pk)
        profile = get_or_create_profile(user)
        profile.verified = bool(request.data.get("verified"))
        profile.save(update_fields=["verified"])
        return Response(UserRoleSerializer(user).data)


class MeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        get_token(request)
        if request.user.is_authenticated:
            return Response({"user": UserSerializer(request.user).data})
        return Response({"user": None})

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data)

