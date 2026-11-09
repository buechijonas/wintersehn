from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("sponsors", views.SponsorViewSet, basename="search-sponsor")

urlpatterns = router.urls + [
    path(
        "settings/",
        views.SearchSettingsViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="search-settings",
    ),
    path(
        "host-ratings/",
        views.HostRatingsViewSet.as_view({"post": "create"}),
        name="search-host-ratings",
    ),
    path(
        "child-protection/",
        views.ChildProtectionViewSet.as_view({"get": "list"}),
        name="search-child-protection",
    ),
]
