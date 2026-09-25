import base64
import hashlib
import hmac
import json
import secrets
import time
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import UserProfile

User = get_user_model()

# `govex` carries the pre-authentik govex user id of migrated accounts.
SCOPE = "openid profile email govex"

MAX_CLOCK_SKEW_SECONDS = 300


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
    return HttpResponseRedirect(f"{settings.GOVEX_PUBLIC_URL}/application/o/authorize/?{urlencode(params)}")


def govex_account(request):
    return HttpResponseRedirect(settings.GOVEX_ACCOUNT_URL)


def fetch_userinfo(code, code_verifier):
    token_response = requests.post(
        f"{settings.GOVEX_INTERNAL_URL}/application/o/token/",
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
        f"{settings.GOVEX_INTERNAL_URL}/application/o/userinfo/",
        headers={"Authorization": f"Bearer {token_response.json()['access_token']}"},
        timeout=10,
    )
    if not userinfo_response.ok:
        return None
    return userinfo_response.json()


def create_user(govex_sub, username, email):
    # Never link to an existing local account by email: govex doesn't verify
    # email addresses, so that would let anyone claim e.g. the admin account.
    # Pre-govex accounts are linked explicitly with `manage.py link_govex_user`.
    user = User(username=username, email=email)
    user.set_unusable_password()
    try:
        user.save()
    except IntegrityError:
        user.username = f"{username}-{govex_sub[:8]}"
        user.save()
    UserProfile.objects.create(user=user, govex_sub=govex_sub)
    return user


def find_profile(govex_sub, legacy_govex_id):
    """The profile linked to this govex identity, linking a pre-authentik
    profile on the identity's first login.

    `legacy_govex_id` comes from the `govex_id` claim, which authentik only
    sets for accounts copied over from the old govex (an attribute users
    can't edit). Each old profile gets linked once, to exactly one identity.
    """
    profile = UserProfile.objects.filter(govex_sub=govex_sub).select_related("user").first()
    if profile is not None or legacy_govex_id is None:
        return profile

    profile = (
        UserProfile.objects.filter(govex_id=legacy_govex_id, govex_sub__isnull=True)
        .select_related("user")
        .first()
    )
    if profile is not None:
        profile.govex_sub = govex_sub
        profile.save(update_fields=["govex_sub"])
    return profile


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

    govex_sub = str(userinfo["sub"])
    email = userinfo.get("email", "")
    username = userinfo.get("preferred_username") or f"govex-{govex_sub[:8]}"

    profile = find_profile(govex_sub, userinfo.get("govex_id"))
    if profile is None:
        user = create_user(govex_sub, username, email)
    else:
        user = profile.user
        sync_user(user, username, email)

    login(request, user)
    return redirect_to_frontend("/")


def valid_govex_signature(request):
    timestamp = request.headers.get("X-Govex-Timestamp", "")
    signature = request.headers.get("X-Govex-Signature", "")
    if not timestamp.isdigit() or abs(time.time() - int(timestamp)) > MAX_CLOCK_SKEW_SECONDS:
        return False
    expected = hmac.new(
        settings.GOVEX_CLIENT_SECRET.encode(),
        f"{timestamp}.".encode() + request.body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@csrf_exempt
@require_POST
def govex_account_deleted(request):
    """Deletes the local account of a govex identity that was deleted in govex.

    govex calls this server-to-server right before it deletes the identity,
    signed with the OAuth client secret both sides share. Accounts that were
    never linked by `sub` yet (migrated, no login since) match by `govex_id`.
    """
    if not valid_govex_signature(request):
        return HttpResponse(status=403)
    try:
        payload = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400)

    profiles = UserProfile.objects.filter(govex_sub=payload.get("sub")).select_related("user")
    users = [profile.user for profile in profiles]
    if payload.get("govex_id") is not None:
        users += [
            profile.user
            for profile in UserProfile.objects.filter(
                govex_id=payload["govex_id"], govex_sub__isnull=True
            ).select_related("user")
        ]
    for user in users:
        user.delete()
    return HttpResponse(status=204)
