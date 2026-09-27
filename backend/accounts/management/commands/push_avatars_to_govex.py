import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from accounts.models import UserProfile


class Command(BaseCommand):
    help = (
        "Copies the avatars picked in wintersehn into govex, where they are "
        "managed now (attributes.settings.meta.avatar). Run it once before "
        "deploying the govex meta sync, since that sync overwrites wintersehn "
        "with whatever govex has. Avatars already set in govex are kept, so "
        "it's safe to re-run. Needs an authentik API token that may edit users."
    )

    def add_arguments(self, parser):
        parser.add_argument("--url", default=settings.GOVEX_INTERNAL_URL)
        parser.add_argument("--token", required=True)
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only report what would happen, don't write to govex.",
        )

    def handle(self, *args, **options):
        self.api = f"{options['url'].rstrip('/')}/api/v3"
        self.headers = {"Authorization": f"Bearer {options['token']}"}

        copied = kept = missing = 0
        for profile in UserProfile.objects.exclude(avatar="").select_related("user"):
            govex_user = self.find_govex_user(profile)
            if govex_user is None:
                missing += 1
                self.stdout.write(f"? {profile.user} has no govex identity - skipped")
                continue

            attributes = govex_user["attributes"]
            meta = attributes.setdefault("settings", {}).setdefault("meta", {})
            if meta.get("avatar"):
                kept += 1
                self.stdout.write(f"= {profile.user} already has '{meta['avatar']}' in govex")
                continue

            meta["avatar"] = profile.avatar
            if not options["dry_run"]:
                self.request("PATCH", f"/core/users/{govex_user['pk']}/", {"attributes": attributes})
            copied += 1
            self.stdout.write(self.style.SUCCESS(f"+ {profile.user}: '{profile.avatar}'"))

        summary = f"{copied} copied, {kept} kept, {missing} without govex identity"
        self.stdout.write(f"{summary} (dry run)" if options["dry_run"] else summary)

    def find_govex_user(self, profile):
        if profile.govex_sub:
            query = {"uuid": profile.govex_sub}
        elif profile.govex_id is not None:
            query = {"attributes": json.dumps({"govex_id": profile.govex_id})}
        else:
            return None
        results = self.request("GET", "/core/users/", params=query)["results"]
        return results[0] if results else None

    def request(self, method, path, body=None, params=None):
        response = requests.request(
            method, f"{self.api}{path}", headers=self.headers, json=body, params=params, timeout=30
        )
        if not response.ok:
            raise CommandError(f"{method} {path} failed with {response.status_code}: {response.text}")
        return response.json()
