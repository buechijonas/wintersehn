from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Sets up the Content-Editoren group and promotes the given user to admin."

    def add_arguments(self, parser):
        parser.add_argument("--admin-username", default="Wintersehn")

    def handle(self, *args, **options):
        permission = Permission.objects.get(
            content_type__app_label="content", codename="change_sitecontent"
        )
        group, created = Group.objects.get_or_create(name="Content-Editoren")
        group.permissions.add(permission)
        self.stdout.write(
            self.style.SUCCESS(
                f"Group 'Content-Editoren' {'created' if created else 'already existed'}, "
                f"has permission '{permission}'."
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
