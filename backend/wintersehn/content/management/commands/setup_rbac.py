from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Sets up the Content-Editoren group and promotes the given user to admin."

    def add_arguments(self, parser):
        parser.add_argument("--admin-username", default="Wintersehn")

    def handle(self, *args, **options):
        codenames = ["change_sitecontent"] + [
            f"{verb}_{key}"
            for key in ("about", "ethos", "cv", "countries", "media")
            for verb in ("add", "view", "change", "delete")
        ]
        permissions = Permission.objects.filter(
            content_type__app_label="content", codename__in=codenames
        )
        group, created = Group.objects.get_or_create(name="Content-Editoren")
        group.permissions.add(*permissions)
        self.stdout.write(
            self.style.SUCCESS(
                f"Group 'Content-Editoren' {'created' if created else 'already existed'}, "
                f"has {permissions.count()} content permissions."
            )
        )

        username = options["admin_username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"User '{username}' not found, skipping.")
            )
            return

        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])
        user.groups.add(group)
        self.stdout.write(
            self.style.SUCCESS(f"User '{username}' is now staff/superuser.")
        )
