from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("roles", views.RoleViewSet, basename="role")
router.register("permissions", views.PermissionViewSet, basename="permission")

urlpatterns = router.urls + [
    path(
        "uploads/",
        views.UploadViewSet.as_view({"post": "create"}),
        name="content-upload",
    ),
    path(
        "images/<str:name>/",
        views.ImageViewSet.as_view({"get": "retrieve"}),
        name="content-image",
    ),
    path(
        "countries/map/",
        views.CountryMapViewSet.as_view({"get": "list"}),
        name="country-map",
    ),
    path(
        "countries/destination/",
        views.DestinationViewSet.as_view({"put": "update", "delete": "destroy"}),
        name="country-destination",
    ),
    path(
        "dashboard/", views.DashboardViewSet.as_view({"get": "list"}), name="dashboard"
    ),
    path(
        "news/footprint/",
        views.FootprintViewSet.as_view({"get": "list"}),
        name="news-footprint",
    ),
    path(
        "<slug:key>/",
        views.SiteContentViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="site-content",
    ),
]
