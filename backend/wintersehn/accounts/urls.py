from django.urls import path
from rest_framework.routers import SimpleRouter

from . import oidc, views

router = SimpleRouter()
router.register("users", views.UserViewSet, basename="user")

urlpatterns = router.urls + [
    path("oidc/login/", oidc.govex_login, name="govex-login"),
    path("oidc/callback/", oidc.govex_callback, name="govex-callback"),
    path("oidc/account/", oidc.govex_account, name="govex-account"),
    path(
        "oidc/account-deleted/",
        oidc.govex_account_deleted,
        name="govex-account-deleted",
    ),
    path(
        "oidc/account-updated/",
        oidc.govex_account_updated,
        name="govex-account-updated",
    ),
    path("logout/", views.LogoutViewSet.as_view({"post": "create"}), name="logout"),
    path("me/", views.MeViewSet.as_view({"get": "list"}), name="me"),
    path(
        "consent/<str:field>/",
        views.ConsentViewSet.as_view({"post": "create"}),
        name="consent-accept",
    ),
]
