from django.db import models


class SiteContent(models.Model):
    key = models.SlugField(unique=True)
    data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("view_about", "Can view Über mich"),
            ("view_ethos", "Can view Ethos"),
            ("view_cv", "Can view Lebenslauf"),
            ("view_countries", "Can view Länder"),
            ("view_media", "Can view Medien (Arbeit)"),
            ("view_admin", "Can view the admin panel"),
            ("manage_permissions", "Can manage role permissions"),
            ("manage_roles", "Can add, rename and delete roles"),
        ]

    def __str__(self):
        return self.key
