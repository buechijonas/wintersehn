import re
from pathlib import Path
from xml.sax.saxutils import escape

from django.conf import settings

UNSAFE = re.compile(r'[\\/:*?"<>|\x00-\x1f]')


def root():
    return Path(settings.LUMON_MEDIA_ROOT)


def clean(name):
    return UNSAFE.sub("", name).strip(" .") or "Unbenannt"


def folder(title, year):
    return clean(f"{title} ({year})" if year else title)


UNIQUE_IDS = {"movie": ("wikidata", "Q{}"), "tvshow": ("tvmaze", "{}")}


def nfo(tag, title, year, catalog_id):
    kind, pattern = UNIQUE_IDS[tag]
    year_tag = f"<year>{year}</year>" if year else ""
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f"<{tag}><title>{escape(title)}</title>{year_tag}"
        f'<uniqueid type="{kind}" default="true">{pattern.format(catalog_id)}</uniqueid></{tag}>\n'
    )


def catalog_id(tag, value):
    return int(value.removeprefix("Q")) if tag == "movie" else int(value)


def movie_path(fields, catalog_id, extension):
    directory = root() / "movies" / folder(fields["title"], fields["year"])
    return (
        directory / f"{directory.name}.{extension}",
        directory / "movie.nfo",
        nfo("movie", fields["title"], fields["year"], catalog_id),
    )


def episode_path(fields, catalog_id, season, episode, extension):
    directory = root() / "shows" / folder(fields["title"], fields["year"])
    name = f"{clean(fields['title'])} S{season:02d}E{episode:02d}.{extension}"
    return (
        directory / f"Season {season:02d}" / name,
        directory / "tvshow.nfo",
        nfo("tvshow", fields["title"], fields["year"], catalog_id),
    )
