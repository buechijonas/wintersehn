import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

from commons import markdown

from ..crypto import blind_digest
from ..fields import EncryptedBinaryField, EncryptedCharField, EncryptedTextField
from .dossier import Dossier, Relationship
from .helpers import bounded


class EventQuerySet(models.QuerySet):
    def with_links(self):
        return self.prefetch_related(
            "dossiers",
            "stances",
            "traits",
            "addictions",
            "references",
            "relationships__dossier",
            "relationships__person",
        )


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    dossiers = models.ManyToManyField(Dossier, related_name="events")
    title = EncryptedCharField(max_length=200)
    date = models.DateField()
    text = EncryptedTextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def link(self, dossier, stances, traits, addictions, references, relationships):
        self.stances.filter(dossier=dossier).update(event=None)
        self.traits.filter(dossier=dossier).update(event=None)
        self.addictions.filter(dossier=dossier).update(event=None)
        self.references.filter(dossier=dossier).update(event=None)
        self.relationships.involving(dossier).update(event=None)
        dossier.stances.matching(stances).update(event=self)
        dossier.traits.matching(traits).update(event=self)
        dossier.addictions.of_kinds(addictions).update(event=self)
        dossier.references.filter(uuid__in=references).update(event=self)
        Relationship.objects.with_persons(dossier, relationships).update(event=self)

    def set_dossiers(self, dossiers):
        self.dossiers.set(dossiers)
        for related in (
            self.stances,
            self.traits,
            self.addictions,
            self.references,
            self.trust_entries,
        ):
            related.exclude(dossier__in=dossiers).update(event=None)
        self.relationships.exclude(
            models.Q(dossier__in=dossiers) | models.Q(person__in=dossiers)
        ).update(event=None)


class EventReferenceKind(models.TextChoices):
    TEXT = "text", "Text"
    CHAT = "chat", "Chat"


class EventReferenceQuerySet(models.QuerySet):
    def with_chat(self):
        return self.prefetch_related(
            "links", "participants", "messages__sender", "messages__target"
        )


class EventReference(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_references"
    )
    kind = models.CharField(max_length=10, choices=EventReferenceKind.choices)
    icon = models.CharField(max_length=50, blank=True, validators=[validate_slug])
    title = EncryptedCharField(max_length=200)
    text = EncryptedTextField(blank=True)
    links = models.ManyToManyField("self", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = EventReferenceQuerySet.as_manager()

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name_plural = "Event references"

    @property
    def html(self):
        return markdown.render(self.text)

    def __str__(self):
        return self.title

    def fight(self):
        participants = self.participants.all()
        attacks = [
            message
            for message in self.messages.all()
            if message.attack and message.target_id
        ]
        health = {participant.pk: participant.health for participant in participants}
        remaining = {}
        for attack in attacks:
            health[attack.target_id] = max(0, health[attack.target_id] - attack.attack)
            remaining[attack.pk] = health[attack.target_id]
        dealt = {
            participant.pk: sum(
                attack.attack
                for attack in attacks
                if attack.sender_id == participant.pk
            )
            for participant in participants
        }
        return {"health": health, "dealt": dealt, "remaining": remaining}


class ChatImageQuerySet(models.QuerySet):
    def store(self, name, data, user):
        image, _ = self.get_or_create(
            digest=blind_digest(data),
            defaults={"name": name, "data": data, "created_by": user},
        )
        return image

    def with_usage(self):
        usage = models.Count("avatars", distinct=True) + models.Count(
            "messages", distinct=True
        )
        return self.defer("data").annotate(usage=usage)

    def unused(self):
        return self.with_usage().filter(usage=0)


class ChatImage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = EncryptedCharField(max_length=200)
    data = EncryptedBinaryField()
    digest = models.CharField(max_length=64, unique=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ChatImageQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.name


class ChatSide(models.TextChoices):
    LEFT = "left", "Left"
    RIGHT = "right", "Right"


class ChatParticipant(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    reference = models.ForeignKey(
        EventReference, on_delete=models.CASCADE, related_name="participants"
    )
    name = EncryptedCharField(max_length=100)
    side = models.CharField(
        max_length=5, choices=ChatSide.choices, default=ChatSide.LEFT
    )
    health = models.PositiveSmallIntegerField(default=100, validators=bounded(1, 1000))
    avatar = models.ForeignKey(
        ChatImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="avatars",
    )
    dossier = models.ForeignKey(
        Dossier, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    reference = models.ForeignKey(
        EventReference, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        ChatParticipant, on_delete=models.CASCADE, related_name="+"
    )
    text = EncryptedTextField(blank=True)
    image = models.ForeignKey(
        ChatImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    attack = models.PositiveSmallIntegerField(default=0, validators=bounded(0, 1000))
    target = models.ForeignKey(
        ChatParticipant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"{self.sender}: {self.text[:40]}"
