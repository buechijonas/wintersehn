import re
from itertools import zip_longest

from . import tmdb
from .models import MediaFile, Title

CATEGORIES = {
    "sci-fi": {
        "label": "Sci-Fi",
        Title.MOVIE: {"with_genres": "878"},
        Title.TV: {"with_genres": "10765"},
    },
    "anime": {
        "label": "Anime",
        Title.MOVIE: {"with_genres": "16", "with_original_language": "ja"},
        Title.TV: {"with_genres": "16", "with_original_language": "ja"},
    },
    "horror": {
        "label": "Horror",
        Title.MOVIE: {"with_genres": "27"},
    },
    "comedy": {
        "label": "Komödie",
        Title.MOVIE: {"with_genres": "35"},
        Title.TV: {"with_genres": "35"},
    },
}
MEDIA_TYPES = [Title.MOVIE, Title.TV]


def year(date):
    return int(date[:4]) if date and date[:4].isdigit() else None


def item(result, media_type, saved):
    return {
        "tmdb_id": result["id"],
        "media_type": media_type,
        "title": result.get("title") or result.get("name") or "",
        "year": year(result.get("release_date") or result.get("first_air_date")),
        "poster": tmdb.image(result.get("poster_path")),
        "saved": saved.get((media_type, result["id"])),
    }


def items(results, media_type, saved):
    return [item(result, media_type, saved) for result in results]


def matches(result, filters):
    genres = {str(genre) for genre in result.get("genre_ids", [])}
    wanted = set(filters.get("with_genres", "").split(",")) - {""}
    language = filters.get("with_original_language")
    return wanted <= genres and (
        not language or result.get("original_language") == language
    )


def discover(media_type, filters, saved):
    results = tmdb.get(
        f"/discover/{media_type}",
        sort_by="popularity.desc",
        watch_region=tmdb.REGION,
        **filters,
    )["results"]
    return items(results, media_type, saved)


def interleave(groups):
    return [entry for row in zip_longest(*groups) for entry in row if entry]


def search(query, category, media_types, saved):
    filters = CATEGORIES[category] if category else {}
    media_types = [
        media_type
        for media_type in media_types
        if not category or media_type in filters
    ]
    if query:
        results = tmdb.get("/search/multi", query=query, include_adult="false")[
            "results"
        ]
        return [
            item(result, result["media_type"], saved)
            for result in results
            if result.get("media_type") in media_types
            and (not category or matches(result, filters[result["media_type"]]))
        ]
    if category:
        groups = [
            discover(media_type, filters[media_type], saved)
            for media_type in media_types
        ]
        return interleave(groups)
    results = tmdb.get("/trending/all/week")["results"]
    return [
        item(result, result["media_type"], saved)
        for result in results
        if result.get("media_type") in media_types
    ]


def browse(media_type, library, saved):
    media = [
        item(details(media_type, tmdb_id), media_type, saved)
        for tmdb_id in MediaFile.objects.library(media_type)
    ]
    rows = [
        {
            "key": "popular",
            "title": "Beliebt",
            "items": items(
                tmdb.get(f"/{media_type}/popular", region=tmdb.REGION)["results"],
                media_type,
                saved,
            ),
        }
    ]
    rows += [
        {
            "key": key,
            "title": category["label"],
            "items": discover(media_type, category[media_type], saved),
        }
        for key, category in CATEGORIES.items()
        if media_type in category
    ]
    if library:
        rows.insert(0, {"key": "library", "title": "Meine Liste", "items": library})
    if media:
        rows.insert(0, {"key": "media", "title": "Mediathek", "items": media})
    featured = next((row["items"][0] for row in rows if row["items"]), None)
    return {
        "featured": (
            detail(media_type, featured["tmdb_id"], saved) if featured else None
        ),
        "rows": rows,
    }


def providers(result):
    region = result.get("watch/providers", {}).get("results", {}).get(tmdb.REGION, {})
    return {
        "link": region.get("link"),
        **{
            kind: [
                {
                    "name": provider["provider_name"],
                    "logo": tmdb.image(provider["logo_path"], "w92"),
                }
                for provider in region.get(kind, [])
            ]
            for kind in ("flatrate", "free", "ads", "rent", "buy")
        },
    }


def details(media_type, tmdb_id):
    return tmdb.get(f"/{media_type}/{tmdb_id}", append_to_response="watch/providers")


def seasons(result):
    return [
        {
            "number": season["season_number"],
            "name": season.get("name") or f"Staffel {season['season_number']}",
            "episodes": season.get("episode_count", 0),
        }
        for season in result.get("seasons", [])
        if season.get("season_number")
    ]


def detail(media_type, tmdb_id, saved):
    result = details(media_type, tmdb_id)
    return {
        **item(result, media_type, saved),
        "media": (
            MediaFile.objects.movie(tmdb_id)
            if media_type == Title.MOVIE
            else MediaFile.objects.next_up(tmdb_id)
        ),
        "overview": result.get("overview", ""),
        "backdrop": tmdb.image(result.get("backdrop_path"), "w1280"),
        "genres": [genre["name"] for genre in result.get("genres", [])],
        "rating": (
            round(result["vote_average"], 1) if result.get("vote_count") else None
        ),
        "runtime": result.get("runtime"),
        "seasons": seasons(result),
        "providers": providers(result),
    }


def title_fields(media_type, tmdb_id):
    result = details(media_type, tmdb_id)
    return {
        "title": result.get("title") or result.get("name") or "",
        "poster_path": result.get("poster_path") or "",
        "year": year(result.get("release_date") or result.get("first_air_date")),
    }


def season_episodes(tmdb_id, number):
    result = tmdb.get(f"/tv/{tmdb_id}/season/{number}")
    available = MediaFile.objects.episodes(tmdb_id, number)
    return [
        {
            "number": episode["episode_number"],
            "title": episode.get("name") or f"Folge {episode['episode_number']}",
            "overview": episode.get("overview", ""),
            "still": tmdb.image(episode.get("still_path"), "w300"),
            "runtime": episode.get("runtime"),
            "air_date": episode.get("air_date"),
            "media": available.get(episode["episode_number"]),
        }
        for episode in result.get("episodes", [])
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


def detect(tmdb_id, filenames, default_season):
    numbers = {entry["number"] for entry in seasons(details("tv", tmdb_id))}
    titles = {}
    detections = []
    for filename in filenames:
        season, episode = parse_episode(filename, default_season)
        if season not in numbers:
            season, episode = None, None
        if season and season not in titles:
            titles[season] = {
                entry["number"]: entry for entry in season_episodes(tmdb_id, season)
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
