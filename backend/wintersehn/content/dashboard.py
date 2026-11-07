import random

from django.utils import timezone

from .footprint import footprint, privacy_section
from .models import SiteContent


def pick(items):
    return random.choice(items) if items else None


def news_section(key):
    sections = (
        item
        for group in SiteContent.objects.data("news", [])
        for item in group["items"]
    )
    return next((section for section in sections if section["key"] == key), {})


def section_items(key):
    return [
        item for group in news_section(key).get("groups", []) for item in group["items"]
    ]


def alternatives():
    return [item for item in section_items("apps") if item.get("replaces")]


def retrospects():
    year = timezone.localdate().year
    return [
        {**entry, "section": item["label"], "years_ago": year - int(entry["year"])}
        for section in SiteContent.objects.data("cv", [])
        for item in section["items"]
        for entry in item.get("timeline", [])
        if entry["year"].isdigit() and int(entry["year"]) < year
    ]


def channels():
    groups = SiteContent.objects.data("media", [])
    return [
        item
        for group in groups
        if not group.get("requiresAuth")
        for item in group["items"]
    ]


def reduction():
    section = privacy_section(SiteContent.objects.data("news", []))
    return footprint(section)["reduction"] if section else None


def stat(label, value, unit=""):
    return {"label": label, "value": value, "unit": unit}


def count(singular, plural, items):
    return stat(singular if len(items) == 1 else plural, len(items))


def dashboard(user):
    return {
        "now": SiteContent.objects.data("now", []),
        "stats": [
            count("Artikel", "Artikeln", SiteContent.objects.data("article", [])),
            count("Kanal", "Kanäle", channels()),
            count("Alternative", "Alternativen", alternatives()),
            stat("weniger Datenspur", reduction(), "%"),
        ],
        "retrospect": (
            pick(retrospects()) if user.has_perm("content.view_cv") else None
        ),
        "alternative": pick(alternatives()),
        "medium": pick(section_items("news")),
    }
