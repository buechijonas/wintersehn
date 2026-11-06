from rest_framework import serializers

from .models import Documentation, Flashcard, Image, Institution, LearningSet, Subject

NAME = {"trim_whitespace": True, "allow_blank": False}


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["uuid", "name", "url"]


class InstitutionSerializer(serializers.ModelSerializer):
    subject_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Institution
        fields = ["uuid", "name", "subject_count"]
        extra_kwargs = {"name": NAME}


class InstitutionRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["uuid", "name"]


class SubjectSerializer(serializers.ModelSerializer):
    documentation_count = serializers.IntegerField(read_only=True)
    learning_set_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Subject
        fields = ["uuid", "name", "documentation_count", "learning_set_count"]
        extra_kwargs = {"name": NAME}


class SubjectRefSerializer(serializers.ModelSerializer):
    institution = InstitutionRefSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = ["uuid", "name", "institution"]


class InstitutionDetailSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = ["uuid", "name", "subjects"]
        extra_kwargs = {"name": NAME}


class DocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = ["uuid", "title", "updated_at"]
        extra_kwargs = {"title": NAME}


class DocumentationDetailSerializer(serializers.ModelSerializer):
    subject = SubjectRefSerializer(read_only=True)

    class Meta:
        model = Documentation
        fields = ["uuid", "title", "body", "html", "updated_at", "subject"]
        extra_kwargs = {"title": NAME}


class LearningSetSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    known_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = LearningSet
        fields = ["uuid", "title", "description", "card_count", "known_count"]
        extra_kwargs = {"title": NAME}


class SubjectDetailSerializer(serializers.ModelSerializer):
    institution = InstitutionRefSerializer(read_only=True)
    documentations = DocumentationSerializer(many=True, read_only=True)
    learning_sets = LearningSetSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ["uuid", "name", "institution", "documentations", "learning_sets"]
        extra_kwargs = {"name": NAME}


class FlashcardSerializer(serializers.ModelSerializer):
    front_image = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Image.objects.all(), allow_null=True, required=False
    )
    back_image = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Image.objects.all(), allow_null=True, required=False
    )
    front_image_url = serializers.CharField(
        source="front_image.url", read_only=True, default=None
    )
    back_image_url = serializers.CharField(
        source="back_image.url", read_only=True, default=None
    )

    class Meta:
        model = Flashcard
        fields = [
            "uuid",
            "front",
            "back",
            "front_image",
            "back_image",
            "front_image_url",
            "back_image_url",
            "last_known",
        ]
        read_only_fields = ["last_known"]

    def validate(self, data):
        current = {"front": "", "front_image": None}
        if self.instance:
            current = {
                "front": self.instance.front,
                "front_image": self.instance.front_image,
            }
        card = {**current, **data}
        if not (card["front"].strip() or card["front_image"]):
            raise serializers.ValidationError(
                {"front": "Die Vorderseite braucht Text oder ein Bild."}
            )
        return data


class LearningSetDetailSerializer(LearningSetSerializer):
    subject = SubjectRefSerializer(read_only=True)
    cards = FlashcardSerializer(many=True, read_only=True)

    class Meta(LearningSetSerializer.Meta):
        fields = [*LearningSetSerializer.Meta.fields, "subject", "cards"]


class OptionSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(
        source="back_image.url", read_only=True, default=None
    )

    class Meta:
        model = Flashcard
        fields = ["uuid", "back", "image_url"]


class QuizCardSerializer(serializers.ModelSerializer):
    front_image_url = serializers.CharField(
        source="front_image.url", read_only=True, default=None
    )
    options = serializers.SerializerMethodField()

    class Meta:
        model = Flashcard
        fields = ["uuid", "front", "front_image_url", "writable", "options"]

    def get_options(self, card):
        return OptionSerializer(card.options(self.context["pool"]), many=True).data


class AnswerSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=["choice", "write"])
    answer = serializers.CharField(allow_blank=True, trim_whitespace=False)


class AnswerResultSerializer(serializers.ModelSerializer):
    back_image_url = serializers.CharField(
        source="back_image.url", read_only=True, default=None
    )

    class Meta:
        model = Flashcard
        fields = ["uuid", "back", "back_image_url"]


class PreviewSerializer(serializers.Serializer):
    body = serializers.CharField(allow_blank=True, trim_whitespace=False)


class DocumentationGroupSerializer(serializers.ModelSerializer):
    items = DocumentationSerializer(source="documentations", many=True)

    class Meta:
        model = Subject
        fields = ["uuid", "name", "items"]


class LearningSetGroupSerializer(serializers.ModelSerializer):
    items = LearningSetSerializer(source="learning_sets", many=True)

    class Meta:
        model = Subject
        fields = ["uuid", "name", "items"]


class DocumentationOverviewSerializer(serializers.ModelSerializer):
    subjects = DocumentationGroupSerializer(many=True)

    class Meta:
        model = Institution
        fields = ["uuid", "name", "subjects"]


class LearningSetOverviewSerializer(serializers.ModelSerializer):
    subjects = LearningSetGroupSerializer(many=True)

    class Meta:
        model = Institution
        fields = ["uuid", "name", "subjects"]
