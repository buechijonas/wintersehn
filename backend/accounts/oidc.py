import base64
import hashlib
import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from .models import UserProfile

User = get_user_model()

SCOPE = "openid profile email"


def code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def redirect_to_frontend(path):
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}{path}")


def govex_login(request):
    """Starts the OIDC Authorization Code + PKCE flow on govex."""
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    request.session["govex_oauth_state"] = state
    request.session["govex_oauth_code_verifier"] = code_verifier

    params = {
        "response_type": "code",
        "client_id": settings.GOVEX_CLIENT_ID,
        "redirect_uri": settings.GOVEX_REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
        "code_challenge": code_challenge(code_verifier),
        "code_challenge_method": "S256",
    }
    return HttpResponseRedirect(f"{settings.GOVEX_PUBLIC_URL}/o/authorize/?{urlencode(params)}")


def govex_account(request):
    return HttpResponseRedirect(f"{settings.GOVEX_PUBLIC_URL}/account")


def fetch_userinfo(code, code_verifier):
    token_response = requests.post(
        f"{settings.GOVEX_INTERNAL_URL}/o/token/",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.GOVEX_REDIRECT_URI,
            "client_id": settings.GOVEX_CLIENT_ID,
            "client_secret": settings.GOVEX_CLIENT_SECRET,
            "code_verifier": code_verifier,
        },
        timeout=10,
    )
    if not token_response.ok:
        return None

    userinfo_response = requests.get(
        f"{settings.GOVEX_INTERNAL_URL}/o/userinfo/",
        headers={"Authorization": f"Bearer {token_response.json()['access_token']}"},
        timeout=10,
    )
    if not userinfo_response.ok:
        return None
    return userinfo_response.json()


def create_user(govex_id, username, email):
    # Never link to an existing local account by email: govex doesn't verify
    # email addresses, so that would let anyone claim e.g. the admin account.
    # Pre-govex accounts are linked explicitly with `manage.py link_govex_user`.
    user = User(username=username, email=email)
    user.set_unusable_password()
    try:
        user.save()
    except IntegrityError:
        user.username = f"{username}-{govex_id}"
        user.save()
    UserProfile.objects.create(user=user, govex_id=govex_id)
    return user


def sync_user(user, username, email):
    if user.username == username and user.email == email:
        return
    user.username, user.email = username, email
    try:
        user.save(update_fields=["username", "email"])
    except IntegrityError:
        user.refresh_from_db()


def govex_callback(request):
    """Exchanges the code with govex server-to-server and logs the matching
    local user in, creating it on first login."""
    expected_state = request.session.pop("govex_oauth_state", None)
    code_verifier = request.session.pop("govex_oauth_code_verifier", None)
    code = request.GET.get("code")
    if not code or not expected_state or request.GET.get("state") != expected_state:
        return redirect_to_frontend("/login?error=oidc_failed")

    userinfo = fetch_userinfo(code, code_verifier)
    if userinfo is None:
        return redirect_to_frontend("/login?error=oidc_failed")

    govex_id = int(userinfo["sub"])
    email = userinfo.get("email", "")
    username = userinfo.get("preferred_username") or f"govex-{govex_id}"

    profile = UserProfile.objects.filter(govex_id=govex_id).select_related("user").first()
    if profile is None:
        user = create_user(govex_id, username, email)
    else:
        user = profile.user
        sync_user(user, username, email)

    login(request, user)
    return redirect_to_frontend("/")
