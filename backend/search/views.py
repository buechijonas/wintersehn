from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SearchSettings
from .serializers import SearchSettingsSerializer


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
