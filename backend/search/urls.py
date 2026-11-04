from django.urls import path

from . import views

urlpatterns = [
    path("settings/", views.SearchSettingsView.as_view(), name="search-settings"),
]
