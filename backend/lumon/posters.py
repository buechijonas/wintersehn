from html import escape
from textwrap import wrap

PALETTES = [
    (("anime", "animation", "zeichentrick"), "#7c3aed", "#ec4899"),
    (("horror",), "#1c1917", "#7f1d1d"),
    (("science", "sci-fi", "fantasy"), "#1e3a8a", "#0ea5e9"),
    (("komödie", "comedy"), "#f59e0b", "#ef4444"),
]
DEFAULT_PALETTE = ("#334155", "#64748b")
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def url(media_type, catalog_id, kind):
    return f"/api/lumon/catalog/{media_type}/{catalog_id}/{kind}/"


def palette(genres):
    words = " ".join(genres).lower()
    return next(
        (
            (start, end)
            for keys, start, end in PALETTES
            if any(key in words for key in keys)
        ),
        DEFAULT_PALETTE,
    )


def gradient(start, end):
    return (
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{start}"/><stop offset="1" stop-color="{end}"/>'
        "</linearGradient></defs>"
    )


def poster(title, year, genres):
    start, end = palette(genres)
    lines = wrap(title, 12)[:5]
    top = 330 - len(lines) * 28
    text = "".join(
        f'<tspan x="36" y="{top + index * 56}">{escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600">'
        f"{gradient(start, end)}"
        '<rect width="400" height="600" fill="url(#g)"/>'
        '<circle cx="310" cy="120" r="70" fill="#fff" fill-opacity=".14"/>'
        '<circle cx="80" cy="520" r="140" fill="#000" fill-opacity=".12"/>'
        f'<text fill="#fff" {FONT} font-size="48" font-weight="700">{text}</text>'
        f'<text x="36" y="560" fill="#fff" fill-opacity=".75" {FONT} font-size="24">'
        f"{year or ''}</text></svg>"
    )


def backdrop(genres):
    start, end = palette(genres)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
        f"{gradient(end, start)}"
        '<rect width="1280" height="720" fill="url(#g)"/>'
        '<circle cx="1000" cy="220" r="260" fill="#fff" fill-opacity=".12"/>'
        '<circle cx="760" cy="640" r="320" fill="#000" fill-opacity=".14"/>'
        "</svg>"
    )
