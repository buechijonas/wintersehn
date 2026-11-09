from django.conf import settings

from commons.http import ServiceUnavailable, fetch


class GovexUnavailable(ServiceUnavailable):
    default_detail = "govex ist nicht erreichbar."


def fetch_users(params):
    response = fetch(
        "get",
        f"{settings.GOVEX_INTERNAL_URL}/api/v3/core/users/",
        error=GovexUnavailable,
        headers={"Authorization": f"Bearer {settings.GOVEX_API_TOKEN}"},
        params={**params, "type": ["internal", "external"]},
    )
    return [account(user) for user in response.json()["results"]]


def account(user):
    return {
        "sub": user["uuid"],
        "username": user["username"],
        "name": user["name"],
        "email": user["email"],
        "avatar": user["attributes"]
        .get("settings", {})
        .get("meta", {})
        .get("avatar", ""),
    }


def search_accounts(query):
    return fetch_users({"search": query, "is_active": "true", "page_size": 10})


def get_account(sub):
    return next(iter(fetch_users({"uuid": sub})), None)
