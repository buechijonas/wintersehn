from functools import cached_property

from django.db import models
from django.utils import timezone


class SiteContentQuerySet(models.QuerySet):
    def data(self, key, default):
        content = self.filter(key=key).first()
        return content.data if content else default


class SiteContent(models.Model):
    key = models.SlugField(unique=True)
    data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    objects = SiteContentQuerySet.as_manager()

    class Meta:
        permissions = [
            ("view_admin", "Can view the admin panel"),
            ("view_monolith", "Can view Monolith"),
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
            ("change_user", "Can update user verification"),
            ("assign_user", "Can assign user roles"),
        ]

    def __str__(self):
        return self.key


class DestinationQuerySet(models.QuerySet):
    def current(self):
        destination = self.first()
        return destination if destination and destination.country else None


class Destination(models.Model):
    icon = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)

    objects = DestinationQuerySet.as_manager()

    def __str__(self):
        return self.icon

    @cached_property
    def country(self):
        sections = SiteContent.objects.data("countries", [])
        matches = (
            {**item, "section": section_index, "item": item_index}
            for section_index, section in enumerate(sections)
            for item_index, item in enumerate(section["items"])
            if item["icon"] == self.icon
        )
        return next(matches, None)

    @property
    def days_left(self):
        return (self.date - timezone.localdate()).days if self.date else None
