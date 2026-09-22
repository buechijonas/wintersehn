from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from accounts.models import UserProfile, get_or_create_profile

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Links an existing wintersehn user to a govex identity, so logging in "
        "via govex lands in that account (keeping its role, avatar, consent). "
        "The govex id is the user's id in govex's django-admin."
    )

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("govex_id", type=int)

    def handle(self, *args, **options):
        user = User.objects.filter(username=options["username"]).first()
        if user is None:
            raise CommandError(f"User '{options['username']}' not found.")

        govex_id = options["govex_id"]
        taken = UserProfile.objects.filter(govex_id=govex_id).exclude(user=user).first()
        if taken:
            raise CommandError(f"govex id {govex_id} is already linked to '{taken.user}'.")

        profile = get_or_create_profile(user)
        profile.govex_id = govex_id
        profile.save(update_fields=["govex_id"])
        user.set_unusable_password()
        user.save(update_fields=["password"])
        self.stdout.write(self.style.SUCCESS(f"'{user}' is now linked to govex id {govex_id}."))
