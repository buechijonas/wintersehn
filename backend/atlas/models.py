import random
import unicodedata
import uuid

from django.conf import settings
from django.db import models
from django.db.models.functions import Collate

from . import markdown

CHOICE_COUNT = 4
NAME_ORDER = Collate("name", "de-CH-x-icu")
TITLE_ORDER = Collate("title", "de-CH-x-icu")


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


class InstitutionQuerySet(models.QuerySet):
    def with_counts(self):
        return self.annotate(subject_count=models.Count("subjects")).order_by(
            NAME_ORDER
        )


class Institution(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = InstitutionQuerySet.as_manager()

    class Meta:
        ordering = [NAME_ORDER]

    def __str__(self):
        return self.name


class SubjectQuerySet(models.QuerySet):
    def with_counts(self):
        return self.annotate(
            documentation_count=models.Count("documentations", distinct=True),
            learning_set_count=models.Count("learning_sets", distinct=True),
        ).order_by(NAME_ORDER)


class Subject(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="subjects"
    )
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SubjectQuerySet.as_manager()

    class Meta:
        ordering = [NAME_ORDER]

    def __str__(self):
        return self.name


class Documentation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="documentations"
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [TITLE_ORDER]

    def __str__(self):
        return self.title

    @property
    def html(self):
        return markdown.render(self.body)


class LearningSetQuerySet(models.QuerySet):
    def with_progress(self):
        return self.annotate(
            card_count=models.Count("cards", distinct=True),
            known_count=models.Count(
                "cards", filter=models.Q(cards__last_known=True), distinct=True
            ),
        ).order_by(TITLE_ORDER)


class LearningSet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="learning_sets"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = LearningSetQuerySet.as_manager()

    class Meta:
        ordering = [TITLE_ORDER]

    def __str__(self):
        return self.title


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    data = models.BinaryField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def url(self):
        return f"/api/atlas/images/{self.uuid}/"


class FlashcardQuerySet(models.QuerySet):
    def for_study(self):
        return self.order_by(
            models.F("last_known").asc(nulls_first=True),
            models.F("reviewed_at").asc(nulls_first=True),
            "position",
        )


class Flashcard(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    learning_set = models.ForeignKey(
        LearningSet, on_delete=models.CASCADE, related_name="cards"
    )
    front = models.TextField(blank=True)
    back = models.TextField(blank=True)
    front_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    back_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    position = models.PositiveIntegerField(default=0)
    known_count = models.PositiveIntegerField(default=0)
    unknown_count = models.PositiveIntegerField(default=0)
    last_known = models.BooleanField(null=True)
    reviewed_at = models.DateTimeField(null=True)

    objects = FlashcardQuerySet.as_manager()

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.front[:50]

    @property
    def writable(self):
        return bool(self.back.strip())

    @property
    def answer_key(self):
        return normalize(self.back)

    def options(self, pool):
        others = {
            card.answer_key or card.uuid: card
            for card in pool
            if card.uuid != self.uuid and card.answer_key != self.answer_key
        }
        choices = random.sample(
            list(others.values()), min(len(others), CHOICE_COUNT - 1)
        )
        return random.sample([self, *choices], len(choices) + 1)

    def is_correct(self, mode, answer):
        if mode == "choice":
            return answer == str(self.uuid)
        return normalize(answer) == self.answer_key

    def answer(self, mode, answer, answered_at):
        correct = self.is_correct(mode, answer)
        if not correct or mode == "write" or not self.writable:
            self.review(correct, answered_at)
        return correct

    def review(self, known, reviewed_at):
        self.last_known = known
        self.reviewed_at = reviewed_at
        if known:
            self.known_count += 1
        else:
            self.unknown_count += 1
        self.save(
            update_fields=["last_known", "reviewed_at", "known_count", "unknown_count"]
        )
