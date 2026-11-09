from django.core.management.base import BaseCommand

from lumon import catalog


class Command(BaseCommand):
    help = "Loads the LUMON series and movie overviews into the cache."

    def handle(self, **options):
        for media_type in catalog.MEDIA_TYPES:
            rows = catalog.browse(media_type, [], {})["rows"]
            self.stdout.write(
                f"{media_type}: {sum(len(row['items']) for row in rows)} Titel"
            )
