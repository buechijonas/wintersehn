from django.conf import settings
from django.db import models

from commons.models import BaseModel, BaseQuerySet, UUIDModel

from . import child_protection


class SearchSettingsQuerySet(BaseQuerySet):
    def apply_acl(self, user):
        return self.filter(user=user)


class SearchSettings(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_settings",
    )
    data = models.JSONField(default=dict)

    objects = SearchSettingsQuerySet.as_manager()

    @property
    def protected_data(self):
        return child_protection.protect(self.user, self.data)


class SponsorQuerySet(BaseQuerySet):
    def apply_acl(self, user):
        return self


class Sponsor(UUIDModel):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SponsorQuerySet.as_manager()

    class Meta:
        ordering = ["created_at"]
