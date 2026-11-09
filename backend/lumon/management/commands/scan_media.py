from xml.etree import ElementTree

from django.core.management.base import BaseCommand

from lumon import catalog, library
from lumon.models import MediaFile, Title, Upload


def identity(nfo):
    root = ElementTree.parse(nfo).getroot()
    kind, _ = library.UNIQUE_IDS[root.tag]
    value = root.findtext(f"uniqueid[@type='{kind}']")
    return library.catalog_id(root.tag, value), root.findtext("title")


def videos(directory):
    return sorted(
        path
        for path in directory.rglob("*")
        if path.suffix.lstrip(".").lower() in Upload.EXTENSIONS
    )


def movie_files(nfo):
    catalog_id, title = identity(nfo)
    return [
        {
            "path": path,
            "media_type": Title.MOVIE,
            "catalog_id": catalog_id,
            "season": None,
            "episode": None,
            "title": title,
        }
        for path in videos(nfo.parent)[:1]
    ]


def episode_files(nfo):
    catalog_id, title = identity(nfo)
    episodes = [
        (path, *catalog.parse_episode(path.name, None)) for path in videos(nfo.parent)
    ]
    return [
        {
            "path": path,
            "media_type": Title.TV,
            "catalog_id": catalog_id,
            "season": season,
            "episode": episode,
            "title": title,
        }
        for path, season, episode in episodes
        if season and episode
    ]


def media_files():
    root = library.root()
    movies = (root / "movies").glob("*/movie.nfo")
    shows = (root / "shows").glob("*/tvshow.nfo")
    return [
        *(file for nfo in movies for file in movie_files(nfo)),
        *(file for nfo in shows for file in episode_files(nfo)),
    ]


class Command(BaseCommand):
    help = "Registers videos in the LUMON media folder by their NFO files."

    def handle(self, **options):
        files = media_files()
        for file in files:
            MediaFile.objects.register(**file)
        self.stdout.write(f"{len(files)} Videos registriert.")
