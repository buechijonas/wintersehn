from django.urls import path

from . import oidc, views

urlpatterns = [
    path("oidc/login/", oidc.govex_login, name="govex-login"),
    path("oidc/callback/", oidc.govex_callback, name="govex-callback"),
    path("oidc/account/", oidc.govex_account, name="govex-account"),
    path(
        "oidc/account-deleted/", oidc.govex_account_deleted, name="govex-account-deleted"
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.MeView.as_view(), name="me"),
    path(
        "consent/<str:field>/", views.ConsentAcceptView.as_view(), name="consent-accept"
    ),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/role/", views.UserRoleView.as_view(), name="user-role"),
    path("users/<int:pk>/verify/", views.UserVerifyView.as_view(), name="user-verify"),
]
