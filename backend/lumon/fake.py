import re
from html import escape
from textwrap import wrap

GENRES = {
    16: "Animation",
    18: "Drama",
    27: "Horror",
    35: "Komödie",
    878: "Science Fiction",
    9648: "Mystery",
    10765: "Sci-Fi & Fantasy",
}
COLORS = [
    (16, "#7c3aed", "#ec4899"),
    (27, "#1c1917", "#7f1d1d"),
    (878, "#1e3a8a", "#0ea5e9"),
    (10765, "#1e3a8a", "#0ea5e9"),
    (35, "#f59e0b", "#ef4444"),
]
DEFAULT_COLORS = ("#334155", "#64748b")
PROVIDERS = {
    "flatrate": [{"provider_name": "Play Suisse", "logo_path": None}],
    "rent": [{"provider_name": "Videoload", "logo_path": None}],
}


def movie(tmdb_id, title, year, genres, language="de", runtime=104):
    return {
        "id": tmdb_id,
        "title": title,
        "release_date": f"{year}-03-14",
        "genre_ids": genres,
        "original_language": language,
        "runtime": runtime,
        "media_type": "movie",
        "poster_path": f"/posters/{tmdb_id}.svg",
        "backdrop_path": f"/backdrops/{tmdb_id}.svg",
    }


def series(tmdb_id, name, year, genres, language="de", seasons=2):
    return {
        "id": tmdb_id,
        "name": name,
        "first_air_date": f"{year}-09-01",
        "genre_ids": genres,
        "original_language": language,
        "number_of_seasons": seasons,
        "media_type": "tv",
        "poster_path": f"/posters/{tmdb_id}.svg",
        "backdrop_path": f"/backdrops/{tmdb_id}.svg",
    }


TITLES = [
    movie(101, "Die Station am Rand", 2021, [878, 18]),
    movie(102, "Kältezone", 2019, [878]),
    movie(103, "Der stille Keller", 2022, [27]),
    movie(104, "Nebelhof", 2018, [27, 9648]),
    movie(105, "Zwei Koffer zu viel", 2023, [35]),
    movie(106, "Hochzeit im Schneesturm", 2020, [35]),
    movie(107, "Sternenpost", 2024, [16, 878], "ja"),
    movie(108, "Der Laternenwald", 2017, [16], "ja"),
    series(201, "Orbitwache", 2022, [10765, 18], seasons=3),
    series(202, "Signal aus der Tiefe", 2020, [10765, 9648]),
    series(203, "Die WG am Bahnhof", 2019, [35], seasons=4),
    series(204, "Bürofrieden", 2023, [35], seasons=1),
    series(205, "Klingen des Mondes", 2021, [16, 10765], "ja", seasons=2),
    series(206, "Kleine Drachenschule", 2018, [16, 35], "ja", seasons=5),
]


def results(titles):
    return {"results": list(titles)}


def of_type(media_type):
    return [title for title in TITLES if title["media_type"] == media_type]


def name(title):
    return title.get("title") or title.get("name")


def seasons(title):
    return [
        {"season_number": number, "name": f"Staffel {number}", "episode_count": 6}
        for number in range(1, title.get("number_of_seasons", 0) + 1)
    ]


def season(title, number):
    return {
        "episodes": [
            {
                "episode_number": episode,
                "name": f"Folge {episode}",
                "overview": f"Folge {episode} der Staffel {number} von {name(title)}.",
                "still_path": None,
                "runtime": 45,
                "air_date": f"{title['first_air_date'][:4]}-09-{episode:02d}",
            }
            for episode in range(1, 7)
        ]
    }


def detail(title):
    return {
        "seasons": seasons(title),
        **title,
        "overview": f"{name(title)} ist ein Beispieltitel für die lokale Entwicklung.",
        "genres": [
            {"id": genre, "name": GENRES[genre]} for genre in title["genre_ids"]
        ],
        "vote_average": 7.4,
        "vote_count": 1,
        "watch/providers": {"results": {"CH": {"link": None, **PROVIDERS}}},
    }


def discover(media_type, params):
    genres = {int(genre) for genre in params.get("with_genres", "").split(",") if genre}
    language = params.get("with_original_language")
    return [
        title
        for title in of_type(media_type)
        if genres <= set(title["genre_ids"])
        and (not language or title["original_language"] == language)
    ]


def get(path, **params):
    if path == "/search/multi":
        query = params["query"].casefold()
        return results(title for title in TITLES if query in name(title).casefold())
    if path == "/trending/all/week":
        return results(TITLES)
    if match := re.fullmatch(r"/discover/(movie|tv)", path):
        return results(discover(match[1], params))
    if match := re.fullmatch(r"/(movie|tv)/popular", path):
        return results(of_type(match[1]))
    if match := re.fullmatch(r"/tv/(\d+)/season/(\d+)", path):
        return season(find(int(match[1])), int(match[2]))
    if match := re.fullmatch(r"/(movie|tv)/(\d+)", path):
        return detail(
            next(title for title in of_type(match[1]) if title["id"] == int(match[2]))
        )
    return {"results": []}


def find(tmdb_id):
    return next((title for title in TITLES if title["id"] == tmdb_id), None)


def colors(title):
    return next(
        ((start, end) for genre, start, end in COLORS if genre in title["genre_ids"]),
        DEFAULT_COLORS,
    )


def poster(title):
    start, end = colors(title)
    lines = wrap(name(title), 12)
    top = 330 - len(lines) * 28
    text = "".join(
        f'<tspan x="36" y="{top + index * 56}">{escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    year = (title.get("release_date") or title.get("first_air_date"))[:4]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{start}"/><stop offset="1" stop-color="{end}"/>'
        "</linearGradient></defs>"
        '<rect width="400" height="600" fill="url(#g)"/>'
        '<circle cx="310" cy="120" r="70" fill="#fff" fill-opacity=".14"/>'
        '<circle cx="80" cy="520" r="140" fill="#000" fill-opacity=".12"/>'
        '<text fill="#fff" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="48" font-weight="700">{text}</text>'
        f'<text x="36" y="560" fill="#fff" fill-opacity=".75" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="24">{year}</text>'
        "</svg>"
    )


def backdrop(title):
    start, end = colors(title)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{end}"/><stop offset="1" stop-color="{start}"/>'
        "</linearGradient></defs>"
        '<rect width="1280" height="720" fill="url(#g)"/>'
        '<circle cx="1000" cy="220" r="260" fill="#fff" fill-opacity=".12"/>'
        '<circle cx="760" cy="640" r="320" fill="#000" fill-opacity=".14"/>'
        "</svg>"
    )
