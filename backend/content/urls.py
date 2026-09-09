from django.urls import path

from . import views

urlpatterns = [
    path("roles/", views.RoleListCreateView.as_view(), name="role-list"),
    path("roles/<int:pk>/", views.RoleDetailView.as_view(), name="role-detail"),
    path("permissions/", views.PermissionListView.as_view(), name="permission-list"),
    path("<slug:key>/", views.SiteContentView.as_view(), name="site-content"),
]
