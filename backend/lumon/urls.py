from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views, viewsets

router = SimpleRouter()
router.register("titles", viewsets.TitleViewSet, basename="lumon-title")
router.register("catalog", viewsets.CatalogViewSet, basename="lumon-catalog")
router.register("media", viewsets.MediaViewSet, basename="lumon-media")
router.register("uploads", viewsets.UploadViewSet, basename="lumon-upload")

urlpatterns = router.urls + [
    path("fake/posters/<int:tmdb_id>.svg", views.fake_poster, name="lumon-fake-poster"),
    path(
        "fake/backdrops/<int:tmdb_id>.svg",
        views.fake_backdrop,
        name="lumon-fake-backdrop",
    ),
]
