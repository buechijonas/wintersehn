from django.contrib import admin

from .models import SiteContent


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ["key", "updated_at"]
    readonly_fields = ["updated_at"]
