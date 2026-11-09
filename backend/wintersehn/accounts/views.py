from django.contrib.auth import get_user_model, logout
from django.http import Http404
from django.middleware.csrf import get_token
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from commons.permissions import ActionPermission
from commons.views import BaseViewSet

from .consent import push_to_govex
from .models import CONSENT_FIELDS, UserConsent, get_or_create_profile
from .serializers import (
    ConsentModelSerializer,
    RoleAssignmentSerializer,
    UserModelSerializer,
    VerificationSerializer,
)

User = get_user_model()


class MeViewSet(BaseViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        get_token(request)
        if not request.user.is_authenticated:
            return Response({"user": None})
        return Response({"user": UserModelSerializer.read(request.user).data})


class LogoutViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsentViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, field):
        if field not in CONSENT_FIELDS:
            raise Http404
        consent = UserConsent.of(request.user)
        consent.accept(field)
        push_to_govex(get_or_create_profile(request.user).govex_sub)
        return Response(ConsentModelSerializer.read(consent).data)


class UserViewSet(mixins.ListModelMixin, BaseViewSet):
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, ActionPermission]
    action_permissions = {
        "list": "content.view_role",
        "role": "content.assign_user",
        "verify": "content.change_user",
    }
    pagination_class = None

    def get_queryset(self):
        return User.objects.order_by("username")

    def change(self, serializer_class, own_message):
        if int(self.kwargs["pk"]) == self.request.user.pk:
            raise ValidationError({"detail": own_message})
        member = self.get_object()
        serializer = serializer_class(
            data=self.request.data, context={"request": self.request, "member": member}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserModelSerializer.list(member).data)

    @action(detail=True, methods=["patch"])
    def role(self, request, pk):
        return self.change(
            RoleAssignmentSerializer, "Du kannst deine eigene Rolle nicht ändern."
        )

    @action(detail=True, methods=["patch"])
    def verify(self, request, pk):
        return self.change(
            VerificationSerializer, "Du kannst deine eigene Verifizierung nicht ändern."
        )
