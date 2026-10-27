from django.urls import path

from . import views

urlpatterns = [
    path("roles/", views.RoleListCreateView.as_view(), name="role-list"),
    path("roles/<int:pk>/", views.RoleDetailView.as_view(), name="role-detail"),
    path("permissions/", views.PermissionListView.as_view(), name="permission-list"),
    path(
        "uploads/", views.ContentImageUploadView.as_view(), name="content-image-upload"
    ),
    path(
        "images/<str:name>/", views.ImageThumbnailView.as_view(), name="content-image-thumbnail"
    ),
    path("countries/map/", views.CountryMapView.as_view(), name="country-map"),
    path(
        "countries/destination/",
        views.DestinationView.as_view(),
        name="country-destination",
    ),
    path("<slug:key>/", views.SiteContentView.as_view(), name="site-content"),
]
