from django.http import HttpResponse
from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commons import images, markdown
from commons.permissions import IsAdmin
from commons.serializers import MarkdownPreviewSerializer
from commons.views import BaseViewSet, CreateModelMixin, UpdateModelMixin

from .models import (
    Documentation,
    Exam,
    Flashcard,
    Image,
    Institution,
    LearningSet,
    Subject,
)
from .serializers import (
    AnswerSerializer,
    DocumentationModelSerializer,
    ExamModelSerializer,
    FlashcardModelSerializer,
    ImageModelSerializer,
    InstitutionModelSerializer,
    LearningSetModelSerializer,
    SubjectModelSerializer,
)


class AtlasViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]

    def create_child(self, serializer_class, queryset, **parent):
        serializer = serializer_class.write(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        child = queryset.get(pk=serializer.save(**parent).pk)
        return Response(
            serializer_class.for_action("retrieve")(child).data,
            status=status.HTTP_201_CREATED,
        )


class InstitutionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    AtlasViewSet,
):
    serializer_class = InstitutionModelSerializer

    def get_queryset(self):
        institutions = Institution.objects.apply_acl(self.request.user)
        return (
            institutions.with_counts()
            if self.action == "list"
            else institutions.detailed()
        )

    @action(detail=True, methods=["post"])
    def subjects(self, request, uuid):
        return self.create_child(
            SubjectModelSerializer,
            Subject.objects.detailed(),
            institution=self.get_object(),
        )


class SubjectViewSet(
    mixins.RetrieveModelMixin, UpdateModelMixin, mixins.DestroyModelMixin, AtlasViewSet
):
    serializer_class = SubjectModelSerializer

    def get_queryset(self):
        return Subject.objects.apply_acl(self.request.user).detailed()

    @action(detail=True, methods=["post"])
    def documentations(self, request, uuid):
        return self.create_child(
            DocumentationModelSerializer,
            Documentation.objects.detailed(),
            subject=self.get_object(),
        )

    @action(detail=True, methods=["post"])
    def exams(self, request, uuid):
        return self.create_child(
            ExamModelSerializer, Exam.objects.detailed(), subject=self.get_object()
        )

    @action(detail=True, methods=["post"], url_path="learning-sets")
    def learning_sets(self, request, uuid):
        return self.create_child(
            LearningSetModelSerializer,
            LearningSet.objects.detailed(),
            subject=self.get_object(),
        )


class DocumentationViewSet(
    mixins.RetrieveModelMixin, UpdateModelMixin, mixins.DestroyModelMixin, AtlasViewSet
):
    serializer_class = DocumentationModelSerializer

    def get_queryset(self):
        return Documentation.objects.apply_acl(self.request.user).detailed()

    def list(self, request):
        institutions = Institution.objects.overview(
            "documentations", Documentation.objects.all()
        )
        return Response(
            InstitutionModelSerializer.documentations(institutions, many=True).data
        )

    @action(detail=False, methods=["post"])
    def preview(self, request):
        serializer = MarkdownPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"html": markdown.render(serializer.validated_data["body"])})


class LearningSetViewSet(
    mixins.RetrieveModelMixin, UpdateModelMixin, mixins.DestroyModelMixin, AtlasViewSet
):
    serializer_class = LearningSetModelSerializer

    def get_queryset(self):
        return LearningSet.objects.apply_acl(self.request.user).detailed()

    def list(self, request):
        institutions = Institution.objects.overview(
            "learning_sets", LearningSet.objects.with_progress()
        )
        return Response(
            InstitutionModelSerializer.learning_sets(institutions, many=True).data
        )

    @action(detail=True)
    def quiz(self, request, uuid):
        cards = list(self.get_object().cards.for_study().with_images())
        return Response(
            FlashcardModelSerializer.quiz(
                cards, many=True, context={"pool": cards}
            ).data
        )

    @action(detail=True, methods=["get", "post"])
    def cards(self, request, uuid):
        learning_set = self.get_object()
        if request.method == "GET":
            cards = learning_set.cards.with_images()
            return Response(FlashcardModelSerializer.read(cards, many=True).data)
        return self.create_child(
            FlashcardModelSerializer,
            Flashcard.objects.with_images(),
            learning_set=learning_set,
            position=learning_set.cards.count(),
        )


class ExamViewSet(
    mixins.RetrieveModelMixin, UpdateModelMixin, mixins.DestroyModelMixin, AtlasViewSet
):
    serializer_class = ExamModelSerializer

    def get_queryset(self):
        return Exam.objects.apply_acl(self.request.user).detailed()


class FlashcardViewSet(UpdateModelMixin, mixins.DestroyModelMixin, AtlasViewSet):
    serializer_class = FlashcardModelSerializer
    http_method_names = ["post", "patch", "delete"]

    def get_queryset(self):
        return Flashcard.objects.apply_acl(self.request.user).with_images()

    @action(detail=True, methods=["post"])
    def answer(self, request, uuid):
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card = self.get_object()
        correct = card.answer(**serializer.validated_data, answered_at=timezone.now())
        return Response(
            {**FlashcardModelSerializer.answer(card).data, "correct": correct}
        )


class ImageViewSet(mixins.RetrieveModelMixin, AtlasViewSet):
    serializer_class = ImageModelSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Image.objects.apply_acl(self.request.user)

    def create(self, request):
        upload = request.FILES.get("file")
        if not upload:
            raise ValidationError({"file": "Keine Datei hochgeladen."})
        image = Image.objects.create(
            name=images.name(upload),
            data=images.encode(upload),
            created_by=request.user,
        )
        return Response(
            ImageModelSerializer.read(image).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, uuid):
        size = request.query_params.get("size", "")
        data = self.get_object().thumbnail(int(size) if size.isdigit() else None)
        response = HttpResponse(data, content_type="image/webp")
        response["Cache-Control"] = "private, max-age=86400"
        return response
