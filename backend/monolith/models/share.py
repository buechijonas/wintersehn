import secrets
import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import RegexValidator
from django.db import models

from wintersehn.accounts.models import UserProfile

from .dossier import Dossier


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
