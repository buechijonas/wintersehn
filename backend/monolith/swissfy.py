import requests
from django.conf import settings
from rest_framework.exceptions import APIException


class SwissfyUnavailable(APIException):
    status_code = 502
    default_detail = "swissfy ist nicht erreichbar."


def fetch(path):
    try:
        response = requests.get(
            f"{settings.SWISSFY_INTERNAL_URL}/api/internal/profiles/{path}",
            headers={"Authorization": f"Bearer {settings.SWISSFY_API_TOKEN}"},
            timeout=10,
        )
    except requests.RequestException as error:
        raise SwissfyUnavailable() from error
    if response.status_code == 404:
        return None
    if not response.ok:
        raise SwissfyUnavailable()
    return response


def get_profile(sub):
    response = fetch(f"{sub}/")
    if not response:
        return None
    profile = response.json()
    return {
        **profile,
        "url": f"{settings.SWISSFY_PUBLIC_URL}/profile/{profile['username']}",
    }


def get_picture(sub):
    return fetch(f"{sub}/picture/")
