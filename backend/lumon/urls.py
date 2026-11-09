from rest_framework.routers import SimpleRouter

from . import viewsets

router = SimpleRouter()
router.register("titles", viewsets.TitleViewSet, basename="lumon-title")
router.register("catalog", viewsets.CatalogViewSet, basename="lumon-catalog")
router.register("media", viewsets.MediaViewSet, basename="lumon-media")
router.register("uploads", viewsets.UploadViewSet, basename="lumon-upload")

urlpatterns = router.urls
