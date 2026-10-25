from django.contrib import admin

from .models import (
    AccessLog,
    Addiction,
    Dossier,
    Event,
    Reference,
    Relationship,
    Share,
    ShareRule,
    Stance,
    Trait,
    Trust,
    TrustEntry,
)


def can_view_monolith(request):
    return request.user.has_perm("content.view_monolith")


class MonolithAccess:
    def has_module_permission(self, request):
        return can_view_monolith(request) and super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        return can_view_monolith(request) and super().has_view_permission(request, obj)

    def has_add_permission(self, request, *args):
        return can_view_monolith(request) and super().has_add_permission(request, *args)

    def has_change_permission(self, request, obj=None):
        return can_view_monolith(request) and super().has_change_permission(
            request, obj
        )

    def has_delete_permission(self, request, obj=None):
        return can_view_monolith(request) and super().has_delete_permission(
            request, obj
        )


class RelationshipInline(MonolithAccess, admin.TabularInline):
    model = Relationship
    fk_name = "dossier"
    extra = 0


class ReferenceInline(MonolithAccess, admin.TabularInline):
    model = Reference
    extra = 0


class AddictionInline(MonolithAccess, admin.TabularInline):
    model = Addiction
    extra = 0


class StanceInline(MonolithAccess, admin.TabularInline):
    model = Stance
    extra = 0


class TraitInline(MonolithAccess, admin.TabularInline):
    model = Trait
    extra = 0


@admin.register(Dossier)
class DossierAdmin(MonolithAccess, admin.ModelAdmin):
    inlines = [
        RelationshipInline,
        ReferenceInline,
        StanceInline,
        TraitInline,
        AddictionInline,
    ]
    list_display = ["title", "created_by", "created_at"]
    readonly_fields = ["created_at"]


@admin.register(Event)
class EventAdmin(MonolithAccess, admin.ModelAdmin):
    list_display = ["title", "date"]
    filter_horizontal = ["dossiers"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Trust)
class TrustAdmin(MonolithAccess, admin.ModelAdmin):
    list_display = ["dossier", "user", "level"]


@admin.register(TrustEntry)
class TrustEntryAdmin(MonolithAccess, admin.ModelAdmin):
    list_display = ["dossier", "user", "conduct", "date"]
    list_filter = ["conduct"]


class ShareRuleInline(MonolithAccess, admin.TabularInline):
    model = ShareRule
    extra = 0


@admin.register(Share)
class ShareAdmin(MonolithAccess, admin.ModelAdmin):
    inlines = [ShareRuleInline]
    list_display = ["dossier", "recipient", "created_by", "created_at"]


@admin.register(AccessLog)
class AccessLogAdmin(MonolithAccess, admin.ModelAdmin):
    list_display = ["created_at", "user", "method", "path", "status"]
    list_filter = ["method", "status"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
