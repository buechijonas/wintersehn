import operator
import secrets
import uuid
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
    URLValidator,
    validate_slug,
)
from django.db import models
from django.db.models.functions import Coalesce, Collate, Greatest, Least

from wintersehn.accounts.models import UserProfile

from .catalog import (
    CATALOG,
    CHARACTER,
    COMPASS,
    CONDUCT_POINTS,
    CONDUCT_TRAITS,
    SPECTRUM,
    WEIGHTS,
)
from .crypto import blind_digest, blind_index, blind_indexes
from .fields import (
    EncryptedBinaryField,
    EncryptedCharField,
    EncryptedDateField,
    EncryptedTextField,
    HashField,
)


class Canton(models.TextChoices):
    AG = "AG", "Aargau"
    AI = "AI", "Appenzell Inner Rhodes"
    AR = "AR", "Appenzell Outer Rhodes"
    BE = "BE", "Bern"
    BL = "BL", "Basel-Country"
    BS = "BS", "Basel-City"
    FR = "FR", "Fribourg"
    GE = "GE", "Geneva"
    GL = "GL", "Glarus"
    GR = "GR", "Grisons"
    JU = "JU", "Jura"
    LU = "LU", "Lucerne"
    NE = "NE", "Neuchâtel"
    NW = "NW", "Nidwalden"
    OW = "OW", "Obwalden"
    SG = "SG", "St. Gall"
    SH = "SH", "Schaffhausen"
    SO = "SO", "Solothurn"
    SZ = "SZ", "Schwyz"
    TG = "TG", "Thurgau"
    TI = "TI", "Ticino"
    UR = "UR", "Uri"
    VD = "VD", "Vaud"
    VS = "VS", "Valais"
    ZG = "ZG", "Zug"
    ZH = "ZH", "Zurich"


class Status(models.TextChoices):
    PARENT = "parent", "Parent"
    SIBLING = "sibling", "Sibling"
    RELATIVE = "relative", "Relative"
    PARTNER = "partner", "Partner"
    FRIEND = "friend", "Friend"
    HOMIE = "homie", "Homie"
    COLLEAGUE = "colleague", "Colleague"
    ACQUAINTANCE = "acquaintance", "Acquaintance"


INVERSE_STATUS = {Status.PARENT: "child"}


class Dossier(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200)
    birthdate = EncryptedDateField(null=True, blank=True)
    street = EncryptedCharField(max_length=200, blank=True)
    postal_code = EncryptedCharField(
        max_length=4,
        blank=True,
        validators=[RegexValidator(r"^\d{4}$", "PLZ muss aus vier Ziffern bestehen.")],
    )
    canton = models.CharField(max_length=2, choices=Canton.choices, blank=True)
    nationality = EncryptedCharField(max_length=100, blank=True)
    ethnicity = EncryptedCharField(max_length=100, blank=True)
    govex_sub = models.CharField(max_length=64, unique=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [Collate("title", "de-CH-x-icu")]
        verbose_name_plural = "Dossiers"

    def __str__(self):
        return self.title


class RelationshipQuerySet(models.QuerySet):
    def of(self, dossier):
        other_title = models.Case(
            models.When(dossier=dossier, then=models.F("person__title")),
            default=models.F("dossier__title"),
        )
        return (
            self.involving(dossier)
            .select_related("dossier", "person")
            .annotate(other_title=other_title)
            .order_by(Collate("other_title", "de-CH-x-icu"))
        )

    def between(self, dossier, person):
        return self.filter(
            models.Q(dossier__uuid=dossier, person__uuid=person)
            | models.Q(dossier__uuid=person, person__uuid=dossier)
        )

    def involving(self, dossier):
        return self.filter(models.Q(dossier=dossier) | models.Q(person=dossier))

    def with_persons(self, dossier, persons):
        return self.filter(
            models.Q(dossier=dossier, person__uuid__in=persons)
            | models.Q(person=dossier, dossier__uuid__in=persons)
        )


class Relationship(models.Model):
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="relationships"
    )
    person = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name="+")
    status = models.CharField(max_length=20, choices=Status.choices, blank=True)
    event = models.ForeignKey(
        "Event",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="relationships",
    )

    objects = RelationshipQuerySet.as_manager()

    class Meta:
        ordering = [Collate("person__title", "de-CH-x-icu")]
        verbose_name_plural = "Relationships"
        constraints = [
            models.UniqueConstraint(
                Least("dossier", "person"),
                Greatest("dossier", "person"),
                name="unique_relationship",
            ),
            models.CheckConstraint(
                condition=~models.Q(dossier=models.F("person")),
                name="relationship_not_self",
            ),
        ]

    def __str__(self):
        return f"{self.dossier} → {self.person}"

    def other(self, dossier):
        return self.person if self.dossier_id == dossier.pk else self.dossier

    def status_for(self, dossier):
        if self.dossier_id == dossier.pk:
            return self.status
        return INVERSE_STATUS.get(self.status, self.status)


def bounded(minimum, maximum):
    return [MinValueValidator(minimum), MaxValueValidator(maximum)]


def mean(values):
    values = [value for value in values if value is not None]
    return round(sum(values) / len(values)) if values else None


class NetworkSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="+",
    )
    attraction = models.PositiveIntegerField(default=20, validators=bounded(0, 100))
    distance = models.PositiveIntegerField(default=180, validators=bounded(0, 1000))
    repulsion = models.PositiveIntegerField(default=800, validators=bounded(0, 20000))
    gravity = models.PositiveIntegerField(default=12, validators=bounded(0, 100))
    untangling = models.PositiveIntegerField(default=30, validators=bounded(0, 100))

    class Meta:
        verbose_name_plural = "Network settings"


class Reference(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="references"
    )
    icon = models.CharField(max_length=50, validators=[validate_slug])
    name = models.CharField(max_length=200)
    url = models.URLField(
        max_length=500, validators=[URLValidator(schemes=["http", "https"])]
    )
    event = models.ForeignKey(
        "Event",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="references",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "References"

    def __str__(self):
        return self.name


def any_of(conditions):
    return reduce(
        operator.or_,
        (models.Q(**condition) for condition in conditions),
        models.Q(pk__in=[]),
    )


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

    def __str__(self):
        return self.title

    def fight(self):
        health = {
            participant.pk: participant.health
            for participant in self.participants.all()
        }
        dealt = defaultdict(int)
        remaining = {}
        for message in self.messages.all():
            if not (message.attack and message.target_id):
                continue
            health[message.target_id] = max(
                0, health[message.target_id] - message.attack
            )
            dealt[message.sender_id] += message.attack
            remaining[message.pk] = health[message.target_id]
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


class Topic(models.TextChoices):
    POLITICS = "politics", "Political position"
    IDEOLOGY = "ideology", "Ideology"
    ECONOMY = "economy", "Economy"
    SOCIETY = "society", "Society"
    MIGRATION = "migration", "Migration"
    DOMESTIC_POLICY = "domestic_policy", "Domestic policy"
    FOREIGN_POLICY = "foreign_policy", "Foreign policy"
    ENVIRONMENT = "environment", "Environment & climate"
    RELIGION = "religion", "Religion"
    VALUES = "values", "Ethics & values"
    USA = "usa", "USA"
    RUSSIA = "russia", "Russia"
    CHINA = "china", "China"
    EU = "eu", "EU"
    ISRAEL = "israel", "Israel"
    PALESTINE = "palestine", "Palestine"


@dataclass
class TopicStance:
    topic: str
    tags: list

    @property
    def value(self):
        return mean(WEIGHTS[self.topic].get(tag) for tag in self.tags)

    @property
    def suggestions(self):
        return {group: list(tags) for group, tags in CATALOG[self.topic].items()}


class StanceQuerySet(models.QuerySet):
    def by_topic(self, dossier):
        tags = defaultdict(list)
        for topic, tag in self.filter(dossier=dossier).values_list("topic", "tag"):
            tags[topic].append(tag)
        return [TopicStance(topic, tags[topic]) for topic in Topic]

    def set_tags(self, dossier, topic, tags):
        stances = self.filter(dossier=dossier, topic=topic)
        stances.exclude(tag_hash__in=blind_indexes(tags)).delete()
        existing = set(stances.values_list("tag", flat=True))
        self.bulk_create(
            Stance(dossier=dossier, topic=topic, tag=tag)
            for tag in tags
            if tag not in existing
        )
        return TopicStance(topic, tags)

    def matching(self, refs):
        return self.filter(
            any_of(
                {"topic": ref["topic"], "tag_hash": blind_index(ref["tag"])}
                for ref in refs
            )
        )

    def summary(self, dossier):
        values = {stance.topic: stance.value for stance in self.by_topic(dossier)}
        return {
            "spectrum": mean(
                sign * values[topic]
                for topic, sign in SPECTRUM.items()
                if values.get(topic) is not None
            ),
            "compass": {
                axis: mean(values.get(topic) for topic in topics)
                for axis, topics in COMPASS.items()
            },
        }


class Stance(models.Model):
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="stances"
    )
    topic = models.CharField(max_length=20, choices=Topic.choices)
    tag = EncryptedCharField(max_length=60)
    tag_hash = HashField("tag")
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stances",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = StanceQuerySet.as_manager()

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name_plural = "Stances"
        constraints = [
            models.UniqueConstraint(
                fields=["dossier", "topic", "tag_hash"], name="unique_stance"
            )
        ]

    def __str__(self):
        return f"{self.dossier} – {self.get_topic_display()}: {self.tag}"


@dataclass
class Character:
    tags: list

    @property
    def suggestions(self):
        return CHARACTER


class TraitQuerySet(models.QuerySet):
    def matching(self, tags):
        return self.filter(tag_hash__in=blind_indexes(tags))

    def character(self, dossier):
        return Character(
            list(self.filter(dossier=dossier).values_list("tag", flat=True))
        )

    def ensure(self, dossier, tags):
        traits = self.filter(dossier=dossier)
        existing = set(traits.values_list("tag", flat=True))
        self.bulk_create(
            Trait(dossier=dossier, tag=tag) for tag in tags if tag not in existing
        )
        return traits.matching(tags)

    def set_tags(self, dossier, tags):
        self.filter(dossier=dossier).exclude(tag_hash__in=blind_indexes(tags)).delete()
        self.ensure(dossier, tags)
        return Character(tags)


class Trait(models.Model):
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="traits"
    )
    tag = EncryptedCharField(max_length=60)
    tag_hash = HashField("tag")
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="traits",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TraitQuerySet.as_manager()

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name_plural = "Traits"
        constraints = [
            models.UniqueConstraint(fields=["dossier", "tag_hash"], name="unique_trait")
        ]

    def __str__(self):
        return f"{self.dossier} – {self.tag}"


class AddictionKind(models.TextChoices):
    ALCOHOL = "alcohol", "Alcohol"
    CANNABIS = "cannabis", "Cannabis"
    CIGARETTES = "cigarettes", "Cigarettes"
    VAPES = "vapes", "Vapes"
    SNUS = "snus", "Snus"
    CAFFEINE = "caffeine", "Caffeine"
    COCAINE = "cocaine", "Cocaine"
    MDMA = "mdma", "MDMA"
    AMPHETAMINES = "amphetamines", "Amphetamines"
    KETAMINE = "ketamine", "Ketamine"
    PSYCHEDELICS = "psychedelics", "Psychedelics"
    OPIOIDS = "opioids", "Opioids"
    SEDATIVES = "sedatives", "Sedatives"
    CASINO = "casino", "Casino"
    SPORTS_BETTING = "sports_betting", "Sports betting"
    GAMING = "gaming", "Gaming"
    SOCIAL_MEDIA = "social_media", "Social media"
    PORNOGRAPHY = "pornography", "Pornography"
    SHOPPING = "shopping", "Shopping"


class Frequency(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    OCCASIONALLY = "occasionally", "Occasionally"
    FORMER = "former", "Former"


class AddictionQuerySet(models.QuerySet):
    def of_kinds(self, kinds):
        return self.filter(kind_hash__in=blind_indexes(kinds))


class Addiction(models.Model):
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="addictions"
    )
    kind = EncryptedCharField(max_length=20, choices=AddictionKind.choices)
    kind_hash = HashField("kind")
    frequency = EncryptedCharField(max_length=20, choices=Frequency.choices)
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="addictions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AddictionQuerySet.as_manager()

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["dossier", "kind_hash"], name="unique_addiction"
            )
        ]

    def __str__(self):
        return f"{self.dossier} – {self.get_kind_display()}"


class TrustQuerySet(models.QuerySet):
    def circles(self, user):
        level = self.filter(user=user, dossier=models.OuterRef("pk")).values("level")
        return Dossier.objects.annotate(level=models.Subquery(level))


class Trust(models.Model):
    LEVELS = 10
    POINTS_PER_LEVEL = 3

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="trusts"
    )
    level = models.PositiveSmallIntegerField(validators=bounded(1, LEVELS))

    objects = TrustQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Trust"
        constraints = [
            models.UniqueConstraint(fields=["user", "dossier"], name="unique_trust")
        ]

    def __str__(self):
        return f"{self.user} → {self.dossier}: {self.level}"

    @classmethod
    def suggested_level(cls, points):
        level = cls.LEVELS - points // cls.POINTS_PER_LEVEL
        return max(1, level) if level <= cls.LEVELS else None


class Conduct(models.TextChoices):
    PROMISE_KEPT = "promise_kept", "Promise kept"
    PROMISE_BROKEN = "promise_broken", "Promise broken"
    PUNCTUAL = "punctual", "Punctual"
    LATE = "late", "Late"
    CANCELLED = "cancelled", "Cancelled last minute"
    SECRET_KEPT = "secret_kept", "Secret kept"
    SECRET_SHARED = "secret_shared", "Secret shared"
    SUPPORTED = "supported", "Supported"
    LET_DOWN = "let_down", "Let down"
    HONEST = "honest", "Honest"
    LIED = "lied", "Lied"
    DEBT_REPAID = "debt_repaid", "Debt repaid"
    DEBT_UNPAID = "debt_unpaid", "Debt unpaid"
    FAULT_ADMITTED = "fault_admitted", "Fault admitted"
    FAULT_DENIED = "fault_denied", "Fault denied"
    COMPETED = "competed", "Turned everything into a competition"


def conduct_points():
    return models.Case(
        *(
            models.When(conduct=conduct, then=models.Value(points))
            for conduct, points in CONDUCT_POINTS.items()
        ),
        default=models.Value(0),
    )


class TrustEntryQuerySet(models.QuerySet):
    def points(self, user):
        total = (
            self.filter(user=user, dossier=models.OuterRef("pk"))
            .values("dossier")
            .annotate(total=models.Sum(conduct_points()))
            .values("total")
        )
        return Dossier.objects.annotate(points=Coalesce(models.Subquery(total), 0))

    def ledger(self, user, dossier):
        entries = (
            self.filter(user=user, dossier=dossier)
            .select_related("event")
            .prefetch_related("traits")
        )
        points = sum(entry.points for entry in entries)
        trust = Trust.objects.filter(user=user, dossier=dossier).first()
        return {
            "points": points,
            "level": trust and trust.level,
            "suggested_level": Trust.suggested_level(points) if entries else None,
            "conducts": CONDUCT_POINTS,
            "conduct_traits": CONDUCT_TRAITS,
            "traits": Trait.objects.character(dossier).tags,
            "entries": entries,
        }

    def impact(self, user, event, dossier):
        entries = (
            self.filter(user=user, event=event, dossier=dossier)
            .select_related("event")
            .prefetch_related("traits")
        )
        return {"points": sum(entry.points for entry in entries), "entries": entries}


class TrustEntry(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="trust_entries"
    )
    conduct = models.CharField(max_length=20, choices=Conduct.choices)
    date = models.DateField()
    text = EncryptedTextField()
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="trust_entries",
    )
    traits = models.ManyToManyField(Trait, blank=True, related_name="trust_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TrustEntryQuerySet.as_manager()

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name_plural = "Trust entries"

    def __str__(self):
        return f"{self.dossier} – {self.get_conduct_display()}"

    @property
    def points(self):
        return CONDUCT_POINTS[self.conduct]


class AccessLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    status = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} {self.method} {self.path} → {self.status}"


class Visibility(models.TextChoices):
    VISIBLE = "visible", "Visible"
    VALUE = "value", "Value redacted"
    FULL = "full", "Fully redacted"


class ShareQuerySet(models.QuerySet):
    def links(self):
        return self.filter(recipient=None).select_related("dossier", "created_by")

    def received_by(self, user):
        subs = UserProfile.objects.filter(user=user, govex_sub__isnull=False)
        return self.filter(
            recipient__govex_sub__in=subs.values("govex_sub")
        ).select_related("dossier", "created_by")


def generate_token():
    return secrets.token_urlsafe(32)


class Share(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    dossier = models.ForeignKey(
        Dossier, on_delete=models.CASCADE, related_name="shares"
    )
    recipient = models.ForeignKey(
        Dossier,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="received_shares",
    )
    name = models.CharField(max_length=100, blank=True)
    token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_token,
        validators=[
            RegexValidator(
                r"^[A-Za-z0-9_-]{6,64}$",
                "Erlaubt sind 6–64 Zeichen: Buchstaben, Ziffern, - und _.",
            )
        ],
    )
    password = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ShareQuerySet.as_manager()

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Shares"
        constraints = [
            models.UniqueConstraint(
                fields=["dossier", "recipient"], name="unique_share"
            )
        ]

    def __str__(self):
        return f"{self.dossier} → {self.recipient or self.name}"

    def set_password(self, raw):
        self.password = make_password(raw) if raw else ""

    def check_password(self, raw):
        return not self.password or check_password(raw, self.password)

    def rule_map(self):
        return dict(self.rules.values_list("target", "visibility"))

    def visibility(self, target):
        return self.rule_map().get(target, Visibility.FULL)

    def set_rules(self, rules):
        self.rules.all().delete()
        ShareRule.objects.bulk_create(
            ShareRule(share=self, target=target, visibility=visibility)
            for target, visibility in rules.items()
            if visibility != Visibility.FULL
        )


class ShareRule(models.Model):
    share = models.ForeignKey(Share, on_delete=models.CASCADE, related_name="rules")
    target = models.CharField(max_length=100)
    visibility = models.CharField(max_length=10, choices=Visibility.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["share", "target"], name="unique_share_rule"
            )
        ]

    def __str__(self):
        return f"{self.share}: {self.target} = {self.visibility}"
