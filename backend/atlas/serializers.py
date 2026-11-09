from rest_framework import serializers

from commons.serializers import UUIDModelSerializer

from .models import (
    Documentation,
    Exam,
    ExamPart,
    Flashcard,
    Image,
    Institution,
    LearningSet,
    Subject,
)

NAME = {"trim_whitespace": True, "allow_blank": False}


def average_field():
    return serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)


def rounded_field():
    return serializers.DecimalField(max_digits=3, decimal_places=1, read_only=True)


def image_url(source):
    return serializers.CharField(source=f"{source}.url", read_only=True, default=None)


def image_field():
    return serializers.SlugRelatedField(
        slug_field="uuid", queryset=Image.objects.all(), allow_null=True, required=False
    )


class InstitutionReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["uuid", "name"]


class SubjectReferenceSerializer(serializers.ModelSerializer):
    institution = InstitutionReferenceSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = ["uuid", "name", "institution"]


class ImageModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        class Meta(UUIDModelSerializer.read.Meta):
            model = Image
            fields = ["uuid", "name", "url"]


class DocumentationModelSerializer(UUIDModelSerializer):
    class list(UUIDModelSerializer.read):
        class Meta(UUIDModelSerializer.read.Meta):
            model = Documentation
            fields = ["uuid", "title", "updated_at"]

    class retrieve(UUIDModelSerializer.read):
        subject = SubjectReferenceSerializer(read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Documentation
            fields = ["uuid", "title", "body", "html", "updated_at", "subject"]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = Documentation
            fields = ["title", "body"]
            extra_kwargs = {"title": NAME}


class FlashcardModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        front_image = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
        back_image = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
        front_image_url = image_url("front_image")
        back_image_url = image_url("back_image")

        class Meta(UUIDModelSerializer.read.Meta):
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

    class write(UUIDModelSerializer.write):
        front_image = image_field()
        back_image = image_field()

        class Meta(UUIDModelSerializer.write.Meta):
            model = Flashcard
            fields = ["front", "back", "front_image", "back_image"]

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

    class option(UUIDModelSerializer.read):
        image_url = image_url("back_image")

        class Meta(UUIDModelSerializer.read.Meta):
            model = Flashcard
            fields = ["uuid", "back", "image_url"]

    class quiz(UUIDModelSerializer.read):
        front_image_url = image_url("front_image")
        options = serializers.SerializerMethodField()

        class Meta(UUIDModelSerializer.read.Meta):
            model = Flashcard
            fields = ["uuid", "front", "front_image_url", "writable", "options"]

        def get_options(self, card):
            return FlashcardModelSerializer.option(
                card.options(self.context["pool"]), many=True
            ).data

    class answer(UUIDModelSerializer.read):
        back_image_url = image_url("back_image")

        class Meta(UUIDModelSerializer.read.Meta):
            model = Flashcard
            fields = ["uuid", "back", "back_image_url"]


class LearningSetModelSerializer(UUIDModelSerializer):
    class list(UUIDModelSerializer.read):
        card_count = serializers.IntegerField(read_only=True)
        known_count = serializers.IntegerField(read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = LearningSet
            fields = ["uuid", "title", "description", "card_count", "known_count"]

    class retrieve(list):
        subject = SubjectReferenceSerializer(read_only=True)
        cards = FlashcardModelSerializer.read(many=True, read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = LearningSet
            fields = [
                "uuid",
                "title",
                "description",
                "card_count",
                "known_count",
                "subject",
                "cards",
            ]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = LearningSet
            fields = ["title", "description"]
            extra_kwargs = {"title": NAME}


class ExamPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamPart
        fields = ["name", "weight", "grade"]
        extra_kwargs = {"name": NAME}


class ExamModelSerializer(UUIDModelSerializer):
    class read(UUIDModelSerializer.read):
        parts = ExamPartSerializer(many=True, read_only=True)
        result = average_field()
        subject = SubjectReferenceSerializer(read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Exam
            fields = [
                "uuid",
                "name",
                "weight",
                "grade",
                "parts",
                "result",
                "tone",
                "subject",
            ]

    class write(UUIDModelSerializer.write):
        parts = ExamPartSerializer(many=True, required=False)

        class Meta(UUIDModelSerializer.write.Meta):
            model = Exam
            fields = ["name", "weight", "grade", "parts"]
            extra_kwargs = {"name": NAME}

        def validate(self, data):
            current = {"grade": None, "parts": []}
            if self.instance:
                current = {
                    "grade": self.instance.grade,
                    "parts": list(self.instance.parts.all()),
                }
            exam = {**current, **data}
            if exam["grade"] is None and not exam["parts"]:
                raise serializers.ValidationError(
                    {"grade": "Gib eine Note oder mindestens eine Teilnote an."}
                )
            return data

        def create(self, validated_data):
            parts = validated_data.pop("parts", [])
            exam = super().create(validated_data)
            exam.replace_parts(parts)
            return exam

        def update(self, instance, validated_data):
            parts = validated_data.pop("parts", None)
            exam = super().update(instance, validated_data)
            if parts is not None:
                exam.replace_parts(parts)
            return exam


class SubjectModelSerializer(UUIDModelSerializer):
    class list(UUIDModelSerializer.read):
        documentation_count = serializers.IntegerField(read_only=True)
        learning_set_count = serializers.IntegerField(read_only=True)
        rounded = rounded_field()

        class Meta(UUIDModelSerializer.read.Meta):
            model = Subject
            fields = [
                "uuid",
                "name",
                "documentation_count",
                "learning_set_count",
                "rounded",
                "tone",
            ]

    class retrieve(UUIDModelSerializer.read):
        institution = InstitutionReferenceSerializer(read_only=True)
        documentations = DocumentationModelSerializer.list(many=True, read_only=True)
        learning_sets = LearningSetModelSerializer.list(many=True, read_only=True)
        exams = ExamModelSerializer.read(many=True, read_only=True)
        average = average_field()
        rounded = rounded_field()

        class Meta(UUIDModelSerializer.read.Meta):
            model = Subject
            fields = [
                "uuid",
                "name",
                "institution",
                "documentations",
                "learning_sets",
                "exams",
                "average",
                "rounded",
                "tone",
            ]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = Subject
            fields = ["name"]
            extra_kwargs = {"name": NAME}

    class documentations(UUIDModelSerializer.read):
        items = DocumentationModelSerializer.list(source="documentations", many=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Subject
            fields = ["uuid", "name", "items"]

    class learning_sets(UUIDModelSerializer.read):
        items = LearningSetModelSerializer.list(source="learning_sets", many=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Subject
            fields = ["uuid", "name", "items"]


class InstitutionModelSerializer(UUIDModelSerializer):
    class list(UUIDModelSerializer.read):
        subject_count = serializers.IntegerField(read_only=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Institution
            fields = ["uuid", "name", "subject_count"]

    class retrieve(UUIDModelSerializer.read):
        subjects = SubjectModelSerializer.list(many=True, read_only=True)
        average = average_field()
        rounded = rounded_field()

        class Meta(UUIDModelSerializer.read.Meta):
            model = Institution
            fields = ["uuid", "name", "subjects", "average", "rounded", "tone"]

    class write(UUIDModelSerializer.write):
        class Meta(UUIDModelSerializer.write.Meta):
            model = Institution
            fields = ["name"]
            extra_kwargs = {"name": NAME}

    class documentations(UUIDModelSerializer.read):
        subjects = SubjectModelSerializer.documentations(many=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Institution
            fields = ["uuid", "name", "subjects"]

    class learning_sets(UUIDModelSerializer.read):
        subjects = SubjectModelSerializer.learning_sets(many=True)

        class Meta(UUIDModelSerializer.read.Meta):
            model = Institution
            fields = ["uuid", "name", "subjects"]


class AnswerSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=["choice", "write"])
    answer = serializers.CharField(allow_blank=True, trim_whitespace=False)
