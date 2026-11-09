import requests
from rest_framework.exceptions import APIException

TIMEOUT = 12
USER_AGENT = "wintersehn (+https://wintersehn.ch)"


class ServiceUnavailable(APIException):
    status_code = 502
    default_detail = "Ein externer Dienst ist nicht erreichbar."


def session():
    client = requests.Session()
    client.headers["User-Agent"] = USER_AGENT
    return client


def fetch(
    method,
    url,
    error=ServiceUnavailable,
    timeout=TIMEOUT,
    missing=False,
    client=None,
    **options,
):
    try:
        response = (client or session()).request(
            method, url, timeout=timeout, **options
        )
        if missing and response.status_code == 404:
            return None
        response.raise_for_status()
    except requests.RequestException as cause:
        raise error() from cause
    return response
