from django.conf import settings
from django.db import models


class UserConsent(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consent"
    )
    privacy = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    disclaimer = models.BooleanField(default=False)

    def __str__(self):
        return f"Consent({self.user})"
