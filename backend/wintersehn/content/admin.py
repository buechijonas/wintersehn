from django.contrib import admin

from .models import Destination, SiteContent


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ["key", "updated_at"]
    readonly_fields = ["updated_at"]


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["icon", "date"]
