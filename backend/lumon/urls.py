from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("titles", views.TitleViewSet, basename="lumon-title")
router.register("catalog", views.CatalogViewSet, basename="lumon-catalog")
router.register("media", views.MediaViewSet, basename="lumon-media")
router.register("uploads", views.UploadViewSet, basename="lumon-upload")

urlpatterns = router.urls
