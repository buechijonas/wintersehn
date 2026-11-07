from xml.etree import ElementTree

from django.core.management.base import BaseCommand

from lumon import catalog, library
from lumon.models import MediaFile, Title, Upload


def identity(nfo):
    root = ElementTree.parse(nfo).getroot()
    return int(root.findtext("uniqueid[@type='tmdb']")), root.findtext("title")


def videos(directory):
    return sorted(
        path
        for path in directory.rglob("*")
        if path.suffix.lstrip(".").lower() in Upload.EXTENSIONS
    )


class Command(BaseCommand):
    help = "Registers videos in the LUMON media folder by their NFO files."

    def handle(self, **options):
        count = 0
        for nfo in (library.root() / "movies").glob("*/movie.nfo"):
            tmdb_id, title = identity(nfo)
            for path in videos(nfo.parent)[:1]:
                MediaFile.objects.register(
                    path,
                    media_type=Title.MOVIE,
                    tmdb_id=tmdb_id,
                    season=None,
                    episode=None,
                    title=title,
                )
                count += 1
        for nfo in (library.root() / "shows").glob("*/tvshow.nfo"):
            tmdb_id, title = identity(nfo)
            for path in videos(nfo.parent):
                season, episode = catalog.parse_episode(path.name, None)
                if season and episode:
                    MediaFile.objects.register(
                        path,
                        media_type=Title.TV,
                        tmdb_id=tmdb_id,
                        season=season,
                        episode=episode,
                        title=title,
                    )
                    count += 1
        self.stdout.write(f"{count} Videos registriert.")
