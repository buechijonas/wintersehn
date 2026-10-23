import hashlib
import hmac
from functools import cache

from cryptography.fernet import Fernet, MultiFernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


@cache
def fernet():
    if not settings.MONOLITH_ENCRYPTION_KEYS:
        raise ImproperlyConfigured("MONOLITH_ENCRYPTION_KEYS must be set.")
    return MultiFernet([Fernet(key) for key in settings.MONOLITH_ENCRYPTION_KEYS])


def encrypt(value):
    return fernet().encrypt(value.encode()).decode()


def decrypt(token):
    return fernet().decrypt(token.encode()).decode()


def blind_index(value):
    if not settings.MONOLITH_HASH_KEY:
        raise ImproperlyConfigured("MONOLITH_HASH_KEY must be set.")
    key = settings.MONOLITH_HASH_KEY.encode()
    return hmac.new(key, value.encode(), hashlib.sha256).hexdigest()


def blind_indexes(values):
    return [blind_index(value) for value in values]
