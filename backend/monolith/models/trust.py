import uuid

from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce

from ..catalog import CONDUCT_POINTS, CONDUCT_TRAITS
from ..fields import EncryptedTextField
from .dossier import Dossier
from .event import Event
from .helpers import bounded
from .profile import Trait


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
