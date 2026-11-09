from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("institutions", views.InstitutionViewSet, basename="atlas-institution")
router.register("subjects", views.SubjectViewSet, basename="atlas-subject")
router.register(
    "documentations", views.DocumentationViewSet, basename="atlas-documentation"
)
router.register(
    "learning-sets", views.LearningSetViewSet, basename="atlas-learning-set"
)
router.register("cards", views.FlashcardViewSet, basename="atlas-card")
router.register("exams", views.ExamViewSet, basename="atlas-exam")
router.register("images", views.ImageViewSet, basename="atlas-image")

urlpatterns = router.urls
