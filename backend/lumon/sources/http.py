import hashlib
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache
from django.db import connections

from commons.http import ServiceUnavailable, fetch

HOUR = 60 * 60
DAY = 24 * HOUR
WEEK = 7 * DAY


class CatalogUnavailable(ServiceUnavailable):
    default_detail = "Der Katalog ist gerade nicht erreichbar."


def get(url, ttl, **params):
    key = (
        "lumon:" + hashlib.sha256(f"{url}{sorted(params.items())}".encode()).hexdigest()
    )
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = fetch(
        "get",
        url,
        error=CatalogUnavailable,
        timeout=30,
        params=params,
        headers={"Accept": "application/sparql-results+json, application/json"},
    ).json()
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
