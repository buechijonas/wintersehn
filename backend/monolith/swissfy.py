from django.conf import settings

from commons.http import ServiceUnavailable, fetch


class SwissfyUnavailable(ServiceUnavailable):
    default_detail = "swissfy ist nicht erreichbar."


def profiles(path):
    return fetch(
        "get",
        f"{settings.SWISSFY_INTERNAL_URL}/api/internal/profiles/{path}",
        error=SwissfyUnavailable,
        missing=True,
        headers={"Authorization": f"Bearer {settings.SWISSFY_API_TOKEN}"},
    )


def get_profile(sub):
    response = profiles(f"{sub}/")
    if not response:
        return None
    profile = response.json()
    return {
        **profile,
        "url": f"{settings.SWISSFY_PUBLIC_URL}/profile/{profile['username']}",
    }


def get_picture(sub):
    return profiles(f"{sub}/picture/")
