import re
from html import unescape

from . import http

API = "https://api.tvmaze.com"
CATALOG_PAGES = 4
GENRES = {
    "sci-fi": "Science-Fiction",
    "anime": "Anime",
    "horror": "Horror",
    "comedy": "Comedy",
}
TAGS = re.compile(r"<[^>]+>")


def text(html):
    return unescape(TAGS.sub("", html or "")).strip()


def year(date):
    return int(date[:4]) if date else None


def image(entry, size="medium"):
    return (entry.get("image") or {}).get(size)


def item(show):
    return {
        "catalog_id": show["id"],
        "media_type": "tv",
        "title": show["name"],
        "year": year(show.get("premiered")),
        "poster": image(show),
    }


def catalog():
    airing = [
        entry["_embedded"]["show"]
        for entry in http.get(f"{API}/schedule/web", http.HOUR)
        if "show" in entry.get("_embedded", {})
    ]
    archive = [
        show
        for page in range(CATALOG_PAGES)
        for show in http.get(f"{API}/shows", http.DAY, page=page)
    ]
    unique = {show["id"]: show for show in archive + airing}
    return sorted(
        unique.values(), key=lambda show: show.get("weight") or 0, reverse=True
    )


def in_category(show, category):
    return not category or GENRES[category] in show.get("genres", [])


def popular(limit=20):
    return [item(show) for show in catalog()[:limit]]


def category(key, limit=20):
    return [item(show) for show in catalog() if in_category(show, key)][:limit]


def search(query, category=None):
    results = http.get(f"{API}/search/shows", http.HOUR, q=query)
    return [
        item(result["show"])
        for result in results
        if in_category(result["show"], category)
    ]


def show(catalog_id):
    return http.get(f"{API}/shows/{catalog_id}", http.HOUR, embed="seasons")


def backdrop(catalog_id):
    images = http.get(f"{API}/shows/{catalog_id}/images", http.DAY)
    background = next(
        (entry for entry in images if entry.get("type") == "background"), None
    )
    return background["resolutions"]["original"]["url"] if background else None


def channel(entry):
    source = entry.get("webChannel") or entry.get("network")
    if not source:
        return None
    return {
        "name": source["name"],
        "link": source.get("officialSite") or entry.get("officialSite"),
    }


def seasons(entry):
    return [
        {
            "number": season["number"],
            "name": f"Staffel {season['number']}",
            "episodes": season.get("episodeOrder") or 0,
        }
        for season in entry["_embedded"]["seasons"]
        if season.get("number")
    ]


def detail(catalog_id):
    entry = show(catalog_id)
    return {
        **item(entry),
        "overview": text(entry.get("summary")),
        "backdrop": backdrop(catalog_id),
        "genres": entry.get("genres", []),
        "rating": (entry.get("rating") or {}).get("average"),
        "runtime": entry.get("averageRuntime"),
        "seasons": seasons(entry),
        "channel": channel(entry),
    }


def episodes(catalog_id, season):
    return [
        {
            "number": episode["number"],
            "title": episode.get("name") or f"Folge {episode['number']}",
            "overview": text(episode.get("summary")),
            "still": image(episode),
            "runtime": episode.get("runtime"),
            "air_date": episode.get("airdate") or None,
        }
        for episode in http.get(f"{API}/shows/{catalog_id}/episodes", http.HOUR)
        if episode.get("season") == season and episode.get("number")
    ]
