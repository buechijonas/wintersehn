import requests
from rest_framework.exceptions import APIException

TIMEOUT = 10


class ServiceUnavailable(APIException):
    status_code = 502
    default_detail = "Ein externer Dienst ist nicht erreichbar."


def fetch(
    method, url, error=ServiceUnavailable, timeout=TIMEOUT, missing=False, **options
):
    try:
        response = requests.request(method, url, timeout=timeout, **options)
        if missing and response.status_code == 404:
            return None
        response.raise_for_status()
    except requests.RequestException as cause:
        raise error() from cause
    return response
