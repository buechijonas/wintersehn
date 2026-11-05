from django.urls import path

from . import views

urlpatterns = [
    path("settings/", views.SearchSettingsView.as_view(), name="search-settings"),
    path("host-ratings/", views.HostRatingsView.as_view(), name="search-host-ratings"),
    path(
        "child-protection/",
        views.ChildProtectionView.as_view(),
        name="search-child-protection",
    ),
    path("sponsors/", views.SponsorListCreateView.as_view(), name="search-sponsors"),
    path(
        "sponsors/<uuid:uuid>/",
        views.SponsorDetailView.as_view(),
        name="search-sponsor",
    ),
]
