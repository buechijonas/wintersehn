import uuid

from django.conf import settings
from django.db import models


class SearchSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_settings",
    )
    data = models.JSONField(default=dict)


class Sponsor(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
