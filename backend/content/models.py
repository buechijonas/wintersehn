from django.db import models


class SiteContent(models.Model):
    key = models.SlugField(unique=True)
    data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("view_admin", "Can view the admin panel"),
            ("add_about", "Can create Über mich entries"),
            ("view_about", "Can view Über mich"),
            ("change_about", "Can update Über mich"),
            ("delete_about", "Can delete Über mich entries"),
            ("add_ethos", "Can create Ethos entries"),
            ("view_ethos", "Can view Ethos"),
            ("change_ethos", "Can update Ethos"),
            ("delete_ethos", "Can delete Ethos entries"),
            ("add_cv", "Can create Lebenslauf entries"),
            ("view_cv", "Can view Lebenslauf"),
            ("change_cv", "Can update Lebenslauf"),
            ("delete_cv", "Can delete Lebenslauf entries"),
            ("add_countries", "Can create Länder entries"),
            ("view_countries", "Can view Länder"),
            ("change_countries", "Can update Länder"),
            ("delete_countries", "Can delete Länder entries"),
            ("add_media", "Can create Medien entries"),
            ("view_media", "Can view Medien (Arbeit)"),
            ("change_media", "Can update Medien (Arbeit)"),
            ("delete_media", "Can delete Medien entries"),
            ("add_permission", "Can create permission assignments"),
            ("change_permission", "Can update permission assignments"),
            ("delete_permission", "Can delete permission assignments"),
            ("add_role", "Can create roles"),
            ("change_role", "Can update roles"),
            ("view_role", "Can view roles"),
            ("delete_role", "Can delete roles"),
        ]

    def __str__(self):
        return self.key
