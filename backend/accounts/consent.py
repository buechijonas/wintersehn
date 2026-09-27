"""wintersehn keeps the consents to its own contracts. govex only shows them,
as a status wintersehn signs here (ES256 JWS) and pushes to govex, so govex
can store it but not forge it."""

import base64
import json
import logging
import time

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from django.conf import settings

from .models import UserConsent, get_or_create_profile

CONSENT_FIELDS = ["privacy", "terms", "disclaimer", "cookies"]
ATTESTATION_FLOW = "govex-attestation"

logger = logging.getLogger(__name__)


def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def consent_of(user):
    record, _ = UserConsent.objects.get_or_create(user=user)
    return {field: getattr(record, field) for field in CONSENT_FIELDS}


def sign(payload):
    key = serialization.load_pem_private_key(settings.CONSENT_PRIVATE_KEY.encode(), None)
    header = b64url(json.dumps({"alg": "ES256", "typ": "JWT"}).encode())
    body = b64url(json.dumps(payload, separators=(",", ":")).encode())
    der = key.sign(f"{header}.{body}".encode(), ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(der)
    return f"{header}.{body}.{b64url(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}"


def attested_consent(attestation):
    """The consent inside the status govex has. Not verified: it is only
    compared with our own records to see if govex is outdated."""
    try:
        body = attestation.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))["consent"]
    except (AttributeError, IndexError, KeyError, ValueError):
        return None


def push_to_govex(user):
    """Hands govex the current, signed status through its public attestation
    flow. Never raises: a failed push is retried on the next login."""
    govex_sub = get_or_create_profile(user).govex_sub
    if not govex_sub:
        return False
    attestation = sign(
        {
            "iss": "wintersehn",
            "sub": govex_sub,
            "consent": consent_of(user),
            "iat": time.time(),
        }
    )
    url = f"{settings.GOVEX_INTERNAL_URL}/api/v3/flows/executor/{ATTESTATION_FLOW}/?query="
    session = requests.Session()
    try:
        session.get(url, headers={"Accept": "application/json"}, timeout=10).raise_for_status()
        response = session.post(
            url,
            json={"component": "ak-stage-prompt", "attestation": attestation},
            headers={
                "Accept": "application/json",
                "X-authentik-CSRF": session.cookies.get("authentik_csrf", ""),
            },
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
    except (requests.RequestException, ValueError):
        logger.warning("consent push to govex failed", exc_info=True, extra={"user": user.pk})
        return False
    if result.get("component") != "xak-flow-redirect":
        logger.warning("govex rejected consent push: %s", result.get("response_errors"))
        return False
    return True
