from django.db.models import Prefetch
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from monolith.images import encode_image, image_name, thumbnail

from . import markdown, serializers
from .models import Documentation, Flashcard, Image, Institution, LearningSet, Subject
from .permissions import CanViewAtlas


class AtlasViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, CanViewAtlas]
    lookup_field = "uuid"

    def created(self, serializer_class, instance):
        return Response(serializer_class(instance).data, status=status.HTTP_201_CREATED)

    def create_child(self, request, serializer_class, **parent):
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.created(serializer_class, serializer.save(**parent))


class EditViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    AtlasViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]


def overview(group_name, queryset):
    groups = Subject.objects.filter(**{f"{group_name}__isnull": False}).distinct()
    return (
        Institution.objects.filter(subjects__in=groups)
        .distinct()
        .prefetch_related(
            Prefetch(
                "subjects",
                queryset=groups.prefetch_related(
                    Prefetch(group_name, queryset=queryset)
                ),
            )
        )
    )


class InstitutionViewSet(ModelViewSet, AtlasViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.action == "list":
            return Institution.objects.with_counts()
        return Institution.objects.prefetch_related(
            Prefetch("subjects", queryset=Subject.objects.with_counts())
        )

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.InstitutionSerializer
        return serializers.InstitutionDetailSerializer

    @action(detail=True, methods=["post"])
    def subjects(self, request, uuid):
        return self.create_child(
            request, serializers.SubjectSerializer, institution=self.get_object()
        )


class SubjectViewSet(EditViewSet):
    queryset = Subject.objects.select_related("institution").prefetch_related(
        "documentations",
        Prefetch("learning_sets", queryset=LearningSet.objects.with_progress()),
    )
    serializer_class = serializers.SubjectDetailSerializer

    @action(detail=True, methods=["post"])
    def documentations(self, request, uuid):
        return self.create_child(
            request,
            serializers.DocumentationDetailSerializer,
            subject=self.get_object(),
        )

    @action(detail=True, methods=["post"], url_path="learning-sets")
    def learning_sets(self, request, uuid):
        return self.create_child(
            request, serializers.LearningSetSerializer, subject=self.get_object()
        )


class DocumentationViewSet(mixins.ListModelMixin, EditViewSet):
    queryset = Documentation.objects.select_related("subject__institution")
    serializer_class = serializers.DocumentationDetailSerializer

    def list(self, request):
        institutions = overview("documentations", Documentation.objects.all())
        return Response(
            serializers.DocumentationOverviewSerializer(institutions, many=True).data
        )

    @action(detail=False, methods=["post"])
    def preview(self, request):
        serializer = serializers.PreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"html": markdown.render(serializer.validated_data["body"])})


class LearningSetViewSet(mixins.ListModelMixin, EditViewSet):
    queryset = (
        LearningSet.objects.with_progress()
        .select_related("subject__institution")
        .prefetch_related("cards__front_image", "cards__back_image")
    )
    serializer_class = serializers.LearningSetDetailSerializer

    def list(self, request):
        institutions = overview("learning_sets", LearningSet.objects.with_progress())
        return Response(
            serializers.LearningSetOverviewSerializer(institutions, many=True).data
        )

    @action(detail=True, methods=["get"])
    def quiz(self, request, uuid):
        cards = list(
            self.get_object()
            .cards.for_study()
            .select_related("front_image", "back_image")
        )
        return Response(
            serializers.QuizCardSerializer(
                cards, many=True, context={"pool": cards}
            ).data
        )

    @action(detail=True, methods=["get", "post"])
    def cards(self, request, uuid):
        learning_set = self.get_object()
        if request.method == "GET":
            cards = learning_set.cards.select_related("front_image", "back_image")
            return Response(serializers.FlashcardSerializer(cards, many=True).data)
        return self.create_child(
            request,
            serializers.FlashcardSerializer,
            learning_set=learning_set,
            position=learning_set.cards.count(),
        )


class FlashcardViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, AtlasViewSet):
    queryset = Flashcard.objects.select_related("front_image", "back_image")
    serializer_class = serializers.FlashcardSerializer
    http_method_names = ["post", "patch", "delete"]

    @action(detail=True, methods=["post"])
    def answer(self, request, uuid):
        serializer = serializers.AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card = self.get_object()
        correct = card.answer(**serializer.validated_data, answered_at=timezone.now())
        result = serializers.AnswerResultSerializer(card).data
        return Response({**result, "correct": correct})


class ImageViewSet(mixins.CreateModelMixin, AtlasViewSet):
    queryset = Image.objects.all()
    serializer_class = serializers.ImageSerializer
    parser_classes = [MultiPartParser]

    def create(self, request):
        upload = request.FILES.get("file")
        if not upload:
            raise ValidationError({"file": "Keine Datei hochgeladen."})
        image = Image.objects.create(
            name=image_name(upload), data=encode_image(upload), created_by=request.user
        )
        return self.created(serializers.ImageSerializer, image)

    def retrieve(self, request, uuid):
        image = self.get_object()
        size = request.query_params.get("size", "")
        data = thumbnail(bytes(image.data), int(size) if size.isdigit() else None)
        response = HttpResponse(data, content_type="image/webp")
        response["Cache-Control"] = "private, max-age=86400"
        return response
