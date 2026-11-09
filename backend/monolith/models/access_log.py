from django.conf import settings
from django.db import models


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
