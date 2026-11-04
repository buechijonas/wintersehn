from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SearchSettings, Sponsor
from .permissions import SponsorsPermission
from .serializers import SearchSettingsSerializer, SponsorSerializer


class SearchSettingsView(APIView):
    def get(self, request):
        search_settings = SearchSettings.objects.filter(user=request.user).first()
        return Response(
            SearchSettingsSerializer(search_settings or SearchSettings()).data
        )

    def put(self, request):
        search_settings, _ = SearchSettings.objects.get_or_create(user=request.user)
        serializer = SearchSettingsSerializer(search_settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SponsorListCreateView(APIView):
    permission_classes = [SponsorsPermission]

    def get(self, request):
        return Response(SponsorSerializer(Sponsor.objects.all(), many=True).data)

    def post(self, request):
        serializer = SponsorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SponsorDetailView(APIView):
    permission_classes = [SponsorsPermission]

    def put(self, request, uuid):
        sponsor = get_object_or_404(Sponsor, uuid=uuid)
        serializer = SponsorSerializer(sponsor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, uuid):
        get_object_or_404(Sponsor, uuid=uuid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
