from django.urls import path

from . import views


def route(url, viewset, actions, name):
    return path(url, viewset.as_view(actions), name=name)


urlpatterns = [
    route(
        "dossiers/",
        views.DossierViewSet,
        {"get": "list", "post": "create"},
        "dossier-list",
    ),
    route(
        "dossiers/<uuid:uuid>/",
        views.DossierViewSet,
        {"get": "retrieve", "patch": "partial_update"},
        "dossier-detail",
    ),
    route(
        "dossiers/<uuid:uuid>/relationships/",
        views.RelationshipViewSet,
        {"get": "list", "post": "create"},
        "dossier-relationships",
    ),
    route(
        "dossiers/<uuid:uuid>/relationships/<uuid:person>/",
        views.RelationshipViewSet,
        {"patch": "partial_update", "delete": "destroy"},
        "dossier-relationship",
    ),
    route(
        "dossiers/<uuid:uuid>/events/",
        views.EventViewSet,
        {"get": "list", "post": "create"},
        "dossier-events",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/",
        views.EventViewSet,
        {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
        "dossier-event",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/links/",
        views.EventViewSet,
        {"put": "links"},
        "dossier-event-links",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/references/",
        views.EventReferenceViewSet,
        {"get": "list", "post": "create"},
        "event-references",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/references/<uuid:reference>/",
        views.EventReferenceViewSet,
        {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
        "event-reference",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/references/<uuid:reference>/participants/",
        views.ChatParticipantViewSet,
        {"post": "create"},
        "event-reference-participants",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/references/<uuid:reference>/participants/<uuid:item>/",
        views.ChatParticipantViewSet,
        {"patch": "partial_update", "delete": "destroy"},
        "event-reference-participant",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/references/<uuid:reference>/messages/",
        views.ChatMessageViewSet,
        {"post": "create"},
        "event-reference-messages",
    ),
    route(
        "dossiers/<uuid:uuid>/events/<uuid:event>/references/<uuid:reference>/messages/<uuid:item>/",
        views.ChatMessageViewSet,
        {"patch": "partial_update", "delete": "destroy"},
        "event-reference-message",
    ),
    route(
        "dossiers/<uuid:uuid>/addictions/",
        views.AddictionViewSet,
        {"get": "list", "post": "create"},
        "dossier-addictions",
    ),
    route(
        "dossiers/<uuid:uuid>/addictions/<str:kind>/",
        views.AddictionViewSet,
        {"patch": "partial_update", "delete": "destroy"},
        "dossier-addiction",
    ),
    route(
        "dossiers/<uuid:uuid>/references/",
        views.ReferenceViewSet,
        {"get": "list", "post": "create"},
        "dossier-references",
    ),
    route(
        "dossiers/<uuid:uuid>/references/<uuid:reference>/",
        views.ReferenceViewSet,
        {"delete": "destroy"},
        "dossier-reference",
    ),
    route(
        "dossiers/<uuid:uuid>/stances/",
        views.StanceViewSet,
        {"get": "list"},
        "dossier-stances",
    ),
    route(
        "dossiers/<uuid:uuid>/stances/summary/",
        views.StanceViewSet,
        {"get": "summary"},
        "dossier-stance-summary",
    ),
    route(
        "dossiers/<uuid:uuid>/stances/<str:topic>/",
        views.StanceViewSet,
        {"put": "update"},
        "dossier-stance",
    ),
    route(
        "dossiers/<uuid:uuid>/character/",
        views.CharacterViewSet,
        {"get": "retrieve", "put": "update"},
        "dossier-character",
    ),
    route(
        "dossiers/<uuid:uuid>/trust/",
        views.TrustViewSet,
        {"get": "entries", "post": "add_entry"},
        "dossier-trust",
    ),
    route(
        "dossiers/<uuid:uuid>/trust/<uuid:entry>/",
        views.TrustViewSet,
        {"delete": "remove_entry"},
        "dossier-trust-entry",
    ),
    route(
        "dossiers/<uuid:uuid>/govex/",
        views.GovexViewSet,
        {"get": "retrieve", "put": "update", "delete": "destroy"},
        "dossier-govex",
    ),
    route(
        "dossiers/<uuid:uuid>/swissfy/",
        views.SwissfyViewSet,
        {"get": "retrieve"},
        "dossier-swissfy",
    ),
    route(
        "dossiers/<uuid:uuid>/swissfy/picture/",
        views.SwissfyViewSet,
        {"get": "picture"},
        "dossier-swissfy-picture",
    ),
    route(
        "dossiers/<uuid:uuid>/shares/",
        views.ShareViewSet,
        {"get": "list", "post": "create"},
        "dossier-shares",
    ),
    route(
        "dossiers/<uuid:uuid>/shares/<uuid:share>/",
        views.ShareViewSet,
        {
            "get": "retrieve",
            "patch": "partial_update",
            "put": "update",
            "delete": "destroy",
        },
        "dossier-share",
    ),
    route(
        "dossiers/<uuid:uuid>/shares/<uuid:share>/preview/",
        views.ShareViewSet,
        {"get": "preview"},
        "dossier-share-preview",
    ),
    route("shared/", views.SharedViewSet, {"get": "list"}, "shared"),
    route(
        "shared/<uuid:share>/",
        views.SharedViewSet,
        {"get": "retrieve"},
        "shared-detail",
    ),
    route(
        "share/<str:token>/", views.SharedLinkViewSet, {"post": "create"}, "shared-link"
    ),
    route(
        "images/", views.ChatImageViewSet, {"get": "list", "post": "create"}, "images"
    ),
    route(
        "images/unused/", views.ChatImageViewSet, {"delete": "unused"}, "images-unused"
    ),
    route(
        "images/<uuid:image>/",
        views.ChatImageViewSet,
        {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
        "image",
    ),
    route("network/", views.NetworkViewSet, {"get": "list"}, "network"),
    route(
        "network/settings/",
        views.NetworkViewSet,
        {"get": "retrieve", "put": "update"},
        "network-settings",
    ),
    route("trust/", views.TrustViewSet, {"get": "list"}, "trust"),
    route(
        "trust/<uuid:uuid>/",
        views.TrustViewSet,
        {"put": "update", "delete": "destroy"},
        "trust-detail",
    ),
    route(
        "markdown/preview/",
        views.MarkdownViewSet,
        {"post": "preview"},
        "markdown-preview",
    ),
    route("govex/", views.GovexViewSet, {"get": "list"}, "govex-search"),
]
