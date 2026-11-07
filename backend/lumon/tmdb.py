import hashlib

import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import APIException

from . import fake

API = "https://api.themoviedb.org/3"
IMAGES = "https://image.tmdb.org/t/p"
LANGUAGE = "de-DE"
REGION = "CH"
CACHE_SECONDS = 60 * 60 * 6


class TmdbUnavailable(APIException):
    status_code = 502
    default_detail = "TMDB ist nicht erreichbar."


def fake_mode():
    return settings.DEBUG and not settings.TMDB_API_KEY


def get(path, **params):
    if fake_mode():
        return fake.get(path, **params)
    if not settings.TMDB_API_KEY:
        raise TmdbUnavailable("Für LUMON ist kein TMDB-API-Key eingerichtet.")
    query = {"language": LANGUAGE, **params}
    key = (
        "lumon:" + hashlib.sha256(f"{path}{sorted(query.items())}".encode()).hexdigest()
    )
    cached = cache.get(key)
    if cached is not None:
        return cached
    try:
        response = requests.get(
            f"{API}{path}",
            params={"api_key": settings.TMDB_API_KEY, **query},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise TmdbUnavailable() from error
    data = response.json()
    cache.set(key, data, CACHE_SECONDS)
    return data


def image(path, size="w342"):
    if not path:
        return None
    return f"/api/lumon/fake{path}" if fake_mode() else f"{IMAGES}/{size}{path}"
