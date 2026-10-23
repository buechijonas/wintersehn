import re
from functools import singledispatch

from rest_framework import serializers

URL_PATTERN = re.compile(r"^(https?://|mailto:)", re.IGNORECASE)
PATH_PATTERN = re.compile(r"^/(?![/\\])[^\s\\\x00-\x1f\x7f]*\Z")

LINK_PATTERNS = {"url": URL_PATTERN, "to": PATH_PATTERN}


@singledispatch
def iter_links(value):
    return iter(())


@iter_links.register
def _(value: dict):
    for field in LINK_PATTERNS.keys() & value.keys():
        yield field, value[field]
    for child in value.values():
        yield from iter_links(child)


@iter_links.register
def _(value: list):
    for child in value:
        yield from iter_links(child)


def is_valid_link(field, link):
    return not link or LINK_PATTERNS[field].match(str(link)) is not None


def validate_links(data):
    invalid = [
        link for field, link in iter_links(data) if not is_valid_link(field, link)
    ]
    if invalid:
        raise serializers.ValidationError(
            f"Ungültiger Link: {invalid[0]}. Erlaubt sind http://, https://, mailto: "
            "und interne Pfade wie /cv."
        )
