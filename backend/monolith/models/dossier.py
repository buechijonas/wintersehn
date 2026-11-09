import uuid

from django.conf import settings
from django.core.validators import RegexValidator, URLValidator, validate_slug
from django.db import models
from django.db.models.functions import Collate, Greatest, Least

from commons.models import BaseQuerySet

from ..fields import EncryptedCharField, EncryptedDateField
from .helpers import bounded


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


class DossierQuerySet(BaseQuerySet):
    def apply_acl(self, user):
        return self if user.has_perm("content.view_monolith") else self.none()


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

    objects = DossierQuerySet.as_manager()

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
