from functools import partial

from .. import posters
from . import http

API = "https://www.wikidata.org/w/api.php"
SPARQL = "https://query.wikidata.org/sparql"
FILM = "Q11424"
ANIME_FILM = "Q20650540"
FILM_TYPES = {FILM, ANIME_FILM, "Q202866", "Q24869", "Q506240", "Q93204", "Q29168811"}
GENRES = {
    "sci-fi": "Q471839",
    "anime": ANIME_FILM,
    "horror": "Q200092",
    "comedy": "Q157443",
}
MINUTES = {"Q7727": 1, "Q11574": 1 / 60, "Q25235": 60}
MIN_SITELINKS = 30
LIMIT = 20
BATCH = 50


def qid(catalog_id):
    return f"Q{catalog_id}"


def entities(ids):
    found = {}
    for start in range(0, len(ids), BATCH):
        found |= http.get(
            API,
            http.WEEK,
            action="wbgetentities",
            ids="|".join(ids[start : start + BATCH]),
            props="labels|descriptions|claims",
            languages="de|en",
            languagefallback="1",
            format="json",
        )["entities"]
    return found


def text(values):
    return (values.get("de") or values.get("en") or {}).get("value", "")


def values(entity, prop):
    return [
        claim["mainsnak"]["datavalue"]["value"]
        for claim in entity.get("claims", {}).get(prop, [])
        if "datavalue" in claim["mainsnak"]
    ]


def references(entity, prop):
    return [value["id"] for value in values(entity, prop)]


def year(entity):
    years = [int(value["time"][1:5]) for value in values(entity, "P577")]
    return min(years) if years else None


def runtime(entity):
    minutes = [
        round(float(value["amount"]) * MINUTES[value["unit"].rsplit("/", 1)[1]])
        for value in values(entity, "P2047")
        if value.get("unit", "").rsplit("/", 1)[1] in MINUTES
    ]
    return minutes[0] if minutes else None


def in_category(entity, category):
    if not category:
        return True
    return GENRES[category] in references(entity, "P31") + references(entity, "P136")


def item(entity):
    catalog_id = int(entity["id"][1:])
    return {
        "catalog_id": catalog_id,
        "media_type": "movie",
        "title": text(entity.get("labels", {})),
        "year": year(entity),
        "poster": posters.url("movie", catalog_id, "poster"),
    }


def films(ids):
    found = entities(ids)
    return [item(found[entity_id]) for entity_id in ids if entity_id in found]


def ranked(category):
    genre = GENRES[category]
    pattern = (
        f"?film wdt:P31 wd:{genre}."
        if genre == ANIME_FILM
        else f"?film wdt:P31 wd:{FILM}; wdt:P136 wd:{genre}."
    )
    query = (
        f"SELECT ?film (MAX(?links) AS ?popularity) WHERE {{ {pattern} "
        f"?film wikibase:sitelinks ?links. FILTER(?links > {MIN_SITELINKS}) }} "
        f"GROUP BY ?film ORDER BY DESC(?popularity) LIMIT {LIMIT}"
    )
    bindings = http.get(SPARQL, http.WEEK, query=query, format="json")["results"][
        "bindings"
    ]
    return [
        (
            binding["film"]["value"].rsplit("/", 1)[1],
            int(binding["popularity"]["value"]),
        )
        for binding in bindings
    ]


def category(key):
    return films([film for film, _ in ranked(key)])


def ranked_or_empty(category):
    try:
        return ranked(category)
    except http.CatalogUnavailable:
        return []


def popular():
    groups = http.parallel([partial(ranked_or_empty, genre) for genre in GENRES])
    popularity = {film: links for group in groups for film, links in group}
    top = sorted(popularity, key=popularity.get, reverse=True)[:LIMIT]
    return films(top)


def search(query, category=None):
    types = "|".join(f"P31={film_type}" for film_type in sorted(FILM_TYPES))
    results = http.get(
        API,
        http.HOUR,
        action="query",
        list="search",
        srsearch=f"{query} haswbstatement:{types}",
        srlimit=LIMIT,
        format="json",
    )["query"]["search"]
    ids = [result["title"] for result in results]
    found = entities(ids)
    return [
        item(found[entity_id])
        for entity_id in ids
        if entity_id in found and in_category(found[entity_id], category)
    ]


def detail(catalog_id):
    entity = entities([qid(catalog_id)])[qid(catalog_id)]
    genre_ids = references(entity, "P136")
    genres = entities(genre_ids) if genre_ids else {}
    return {
        **item(entity),
        "overview": text(entity.get("descriptions", {})),
        "backdrop": posters.url("movie", catalog_id, "backdrop"),
        "genres": [
            text(genres[genre].get("labels", {}))
            for genre in genre_ids
            if genre in genres
        ],
        "rating": None,
        "runtime": runtime(entity),
        "seasons": [],
        "channel": None,
    }
