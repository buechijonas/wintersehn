from rest_framework.routers import SimpleRouter

from . import viewsets

router = SimpleRouter()
router.register(
    "institutions", viewsets.InstitutionViewSet, basename="atlas-institution"
)
router.register("subjects", viewsets.SubjectViewSet, basename="atlas-subject")
router.register(
    "documentations", viewsets.DocumentationViewSet, basename="atlas-documentation"
)
router.register(
    "learning-sets", viewsets.LearningSetViewSet, basename="atlas-learning-set"
)
router.register("cards", viewsets.FlashcardViewSet, basename="atlas-card")
router.register("images", viewsets.ImageViewSet, basename="atlas-image")

urlpatterns = router.urls
