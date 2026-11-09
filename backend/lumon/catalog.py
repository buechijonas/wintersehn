import re
from functools import partial
from itertools import zip_longest

from . import posters
from .models import MediaFile, Title
from .sources import tvmaze, wikidata
from .sources.http import CatalogUnavailable, parallel

SOURCES = {Title.MOVIE: wikidata, Title.TV: tvmaze}
MEDIA_TYPES = [Title.MOVIE, Title.TV]
CATEGORIES = {
    "sci-fi": "Sci-Fi",
    "anime": "Anime",
    "horror": "Horror",
    "comedy": "Komödie",
}


def mark(entries, saved):
    return [
        {**entry, "saved": saved.get((entry["media_type"], entry["catalog_id"]))}
        for entry in entries
    ]


def interleave(groups):
    return [entry for row in zip_longest(*groups) for entry in row if entry]


def results(source, query, category):
    if query:
        return source.search(query, category)
    if category:
        return source.category(category)
    return source.popular()


def search(query, category, media_types, saved):
    groups = parallel(
        [
            partial(results, SOURCES[media_type], query, category)
            for media_type in media_types
        ]
    )
    return mark(interleave(groups), saved)


def row(key, title, load, saved):
    try:
        entries = load()
    except CatalogUnavailable:
        entries = []
    return {"key": key, "title": title, "items": mark(entries, saved)}


def details(media_type, catalog_id):
    return SOURCES[media_type].detail(catalog_id)


def media(media_type, catalog_id):
    if media_type == Title.MOVIE:
        return MediaFile.objects.movie(catalog_id)
    return MediaFile.objects.next_up(catalog_id)


def detail(media_type, catalog_id, saved):
    result = details(media_type, catalog_id)
    return {**mark([result], saved)[0], "media": media(media_type, catalog_id)}


def featured(media_type, rows, saved):
    first = next((row["items"][0] for row in rows if row["items"]), None)
    if not first:
        return None
    try:
        return detail(media_type, first["catalog_id"], saved)
    except CatalogUnavailable:
        return None


def library_items(media_type, saved):
    return mark(
        [
            details(media_type, catalog_id)
            for catalog_id in MediaFile.objects.library(media_type)
        ],
        saved,
    )


def browse(media_type, library, saved):
    source = SOURCES[media_type]
    rows = parallel(
        [partial(row, "popular", "Beliebt", source.popular, saved)]
        + [
            partial(row, key, label, partial(source.category, key), saved)
            for key, label in CATEGORIES.items()
        ]
    )
    if library:
        rows.insert(0, {"key": "library", "title": "Meine Liste", "items": library})
    media_row = row("media", "Mediathek", partial(library_items, media_type, saved), {})
    if media_row["items"]:
        rows.insert(0, media_row)
    return {"featured": featured(media_type, rows, saved), "rows": rows}


def artwork(media_type, catalog_id, kind):
    result = details(media_type, catalog_id)
    if kind == "backdrop":
        return posters.backdrop(result["genres"])
    return posters.poster(result["title"], result["year"], result["genres"])


def season_episodes(catalog_id, number):
    available = MediaFile.objects.episodes(catalog_id, number)
    return [
        {**episode, "media": available.get(episode["number"])}
        for episode in tvmaze.episodes(catalog_id, number)
    ]


EPISODE_PATTERNS = [
    re.compile(r"s(?P<season>\d{1,2})[ ._-]*e(?P<episode>\d{1,3})", re.IGNORECASE),
    re.compile(r"(?<!\d)(?P<season>\d{1,2})x(?P<episode>\d{1,3})(?!\d)", re.IGNORECASE),
    re.compile(
        r"staffel[ ._-]*(?P<season>\d{1,2}).*?(?:folge|episode|e)[ ._-]*(?P<episode>\d{1,3})",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:folge|episode|ep|e)[ ._-]*(?P<episode>\d{1,3})(?!\d)", re.IGNORECASE
    ),
]


def parse_episode(filename, default_season):
    for pattern in EPISODE_PATTERNS:
        if match := pattern.search(filename):
            season = match.groupdict().get("season")
            return int(season) if season else default_season, int(match["episode"])
    return default_season, None


def detect(catalog_id, filenames, default_season):
    numbers = {entry["number"] for entry in tvmaze.detail(catalog_id)["seasons"]}
    titles = {}
    detections = []
    for filename in filenames:
        season, episode = parse_episode(filename, default_season)
        if season not in numbers:
            season, episode = None, None
        if season and season not in titles:
            titles[season] = {
                entry["number"]: entry for entry in season_episodes(catalog_id, season)
            }
        known = titles.get(season, {}).get(episode)
        detections.append(
            {
                "filename": filename,
                "season": season,
                "episode": episode if known else None,
                "title": known["title"] if known else None,
                "exists": bool(known and known["media"]),
            }
        )
    return detections


def title_fields(media_type, catalog_id):
    result = details(media_type, catalog_id)
    return {
        "title": result["title"],
        "year": result["year"],
        "poster": result["poster"] or "",
    }
