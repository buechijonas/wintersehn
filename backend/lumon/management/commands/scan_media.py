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


class Command(BaseCommand):
    help = "Registers videos in the LUMON media folder by their NFO files."

    def handle(self, **options):
        count = 0
        for nfo in (library.root() / "movies").glob("*/movie.nfo"):
            catalog_id, title = identity(nfo)
            for path in videos(nfo.parent)[:1]:
                MediaFile.objects.register(
                    path,
                    media_type=Title.MOVIE,
                    catalog_id=catalog_id,
                    season=None,
                    episode=None,
                    title=title,
                )
                count += 1
        for nfo in (library.root() / "shows").glob("*/tvshow.nfo"):
            catalog_id, title = identity(nfo)
            for path in videos(nfo.parent):
                season, episode = catalog.parse_episode(path.name, None)
                if season and episode:
                    MediaFile.objects.register(
                        path,
                        media_type=Title.TV,
                        catalog_id=catalog_id,
                        season=season,
                        episode=episode,
                        title=title,
                    )
                    count += 1
        self.stdout.write(f"{count} Videos registriert.")
