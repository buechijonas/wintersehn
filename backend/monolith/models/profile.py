from dataclasses import dataclass

from django.db import models

from ..catalog import CATALOG, CHARACTER, COMPASS, SPECTRUM, WEIGHTS
from ..crypto import blind_index, blind_indexes
from ..fields import EncryptedCharField, HashField
from .dossier import Dossier
from .event import Event
from .helpers import any_of, mean


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
        stances = list(self.filter(dossier=dossier).values_list("topic", "tag"))
        return [
            TopicStance(topic, [tag for tagged, tag in stances if tagged == topic])
            for topic in Topic
        ]

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
