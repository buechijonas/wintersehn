from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from commons.permissions import IsAdmin
from commons.views import BaseViewSet, CreateModelMixin, UpdateModelMixin

from . import child_protection, lookalike, observatory
from .models import SearchSettings, Sponsor
from .serializers import (
    HostRatingsRequestSerializer,
    SearchSettingsModelSerializer,
    SponsorModelSerializer,
)
from .throttling import HostRatingsThrottle


class SearchSettingsViewSet(mixins.RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    serializer_class = SearchSettingsModelSerializer

    def get_queryset(self):
        return SearchSettings.objects.apply_acl(self.request.user)

    def get_object(self):
        return self.get_queryset().first() or SearchSettings(user=self.request.user)


class ChildProtectionViewSet(BaseViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        return Response(
            {
                "required": child_protection.is_required(request.user),
                "domains": child_protection.DOMAINS,
            }
        )


class SponsorViewSet(
    mixins.ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    serializer_class = SponsorModelSerializer
    permission_classes = [IsAdmin]
    permission_action_classes = {"list": [AllowAny]}
    lookup_field = "uuid"

    def get_queryset(self):
        return Sponsor.objects.apply_acl(self.request.user)


class HostRatingsViewSet(BaseViewSet):
    permission_classes = [AllowAny]
    throttle_classes = [HostRatingsThrottle]

    def create(self, request):
        params = HostRatingsRequestSerializer(data=request.data)
        params.is_valid(raise_exception=True)
        hosts = sorted(set(params.validated_data["hosts"]))
        ratings = observatory.ratings(hosts)
        flags = lookalike.lookalikes(hosts)
        return Response(
            {
                "hosts": {
                    host: {**flags.get(host, {}), **ratings.get(host, {})}
                    for host in hosts
                    if host in flags or host in ratings
                }
            }
        )
