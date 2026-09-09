import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from content.rbac import managed_permissions_queryset

User = get_user_model()

DEFAULT_USERNAME = "admin"
DEFAULT_EMAIL = "admin@wintersehn.ch"
DEFAULT_PASSWORD = "admin"
ADMIN_ROLE_NAME = "Admin"


class Command(BaseCommand):
    help = (
        "Bootstraps initial project setup: creates the 'Admin' role with every "
        "managed permission, and an admin user assigned to it with superuser "
        "rights. Safe to re-run - if the admin user already exists, only its "
        "role/staff/superuser status is (re-)ensured, its password is left alone."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", default=os.environ.get("ADMIN_USERNAME", DEFAULT_USERNAME)
        )
        parser.add_argument("--email", default=os.environ.get("ADMIN_EMAIL", DEFAULT_EMAIL))
        parser.add_argument(
            "--password", default=os.environ.get("ADMIN_PASSWORD", DEFAULT_PASSWORD)
        )

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        with transaction.atomic():
            group, group_created = Group.objects.get_or_create(name=ADMIN_ROLE_NAME)
            group.permissions.set(managed_permissions_queryset())
            self.stdout.write(
                self.style.SUCCESS(
                    f"Role '{ADMIN_ROLE_NAME}' {'created' if group_created else 'already existed'} "
                    "with every managed permission."
                )
            )

            user, user_created = User.objects.get_or_create(
                username=username, defaults={"email": email}
            )
            if user_created:
                user.email = email
                user.set_password(password)
                self.stdout.write(
                    self.style.SUCCESS(f"Admin user '{username}' created with the given password.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User '{username}' already exists - leaving email/password untouched, "
                        "only ensuring role and superuser rights."
                    )
                )

            user.is_staff = True
            user.is_superuser = True
            user.save()
            user.groups.set([group])

        self.stdout.write(
            self.style.SUCCESS(
                f"'{username}' is now staff/superuser and assigned to the '{ADMIN_ROLE_NAME}' role."
            )
        )
