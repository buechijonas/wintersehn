import hashlib
from concurrent.futures import ThreadPoolExecutor

import requests
from django.core.cache import cache
from django.db import connections
from rest_framework.exceptions import APIException

USER_AGENT = "LUMON/0.1 (https://lumon.wintersehn.ch)"
HOUR = 60 * 60
DAY = 24 * HOUR
WEEK = 7 * DAY


class CatalogUnavailable(APIException):
    status_code = 502
    default_detail = "Der Katalog ist gerade nicht erreichbar."


def get(url, ttl, **params):
    key = (
        "lumon:" + hashlib.sha256(f"{url}{sorted(params.items())}".encode()).hexdigest()
    )
    cached = cache.get(key)
    if cached is not None:
        return cached
    try:
        response = requests.get(
            url,
            params=params,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/sparql-results+json, application/json",
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise CatalogUnavailable() from error
    data = response.json()
    cache.set(key, data, ttl)
    return data


def run(call):
    try:
        return call()
    finally:
        connections.close_all()


def parallel(calls):
    with ThreadPoolExecutor(len(calls)) as pool:
        return list(pool.map(run, calls))
