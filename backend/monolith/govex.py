import requests
from django.conf import settings
from rest_framework.exceptions import APIException


class GovexUnavailable(APIException):
    status_code = 502
    default_detail = "govex ist nicht erreichbar."


def fetch_users(params):
    try:
        response = requests.get(
            f"{settings.GOVEX_INTERNAL_URL}/api/v3/core/users/",
            headers={"Authorization": f"Bearer {settings.GOVEX_API_TOKEN}"},
            params={**params, "type": ["internal", "external"]},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise GovexUnavailable() from error
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
