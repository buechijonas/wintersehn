from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from wintersehn.accounts.models import CONSENT_FIELDS, UserConsent, UserProfile


def create_user(username, *codenames, verified=True, consent=False, **profile):
    user = get_user_model().objects.create_user(username)
    UserProfile.objects.create(user=user, verified=verified, **profile)
    if consent:
        UserConsent.objects.create(
            user=user, **{field: True for field in CONSENT_FIELDS}
        )
    user.user_permissions.add(*Permission.objects.filter(codename__in=codenames))
    return user


def create_admin(username="admin", *codenames, **options):
    return create_user(username, "view_admin", *codenames, **options)
