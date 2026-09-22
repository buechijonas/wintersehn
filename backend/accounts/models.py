from django.conf import settings
from django.db import models

AVATAR_CHOICES = [
    "bee",
    "bison",
    "camel",
    "cat",
    "chameleon",
    "crab",
    "deer",
    "dog",
    "dolphin",
    "duck",
    "elephant",
    "fish",
    "flamingo",
    "frog",
    "giraffe",
    "hedgehog",
    "hen",
    "hermit-crab",
    "hippopotamus",
    "horse",
    "jellyfish",
    "kangaroo",
    "kiwi",
    "koala",
    "lion",
    "llama",
    "lobster",
    "meerkat",
    "monkey",
    "octopus",
    "ostrich",
    "owl",
    "panda-bear",
    "parrot",
    "penguin",
    "pig",
    "rabbit",
    "seahorse",
    "seal",
    "shark",
    "sheep",
    "snail",
    "snake",
    "squid",
    "squirrel",
    "swan",
    "toucan",
    "turtle",
    "walrus",
    "whale",
]


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.CharField(
        max_length=20, blank=True, default="", choices=[(a, a) for a in AVATAR_CHOICES]
    )
    verified = models.BooleanField(default=False)
    # The `sub` claim of this user's govex identity.
    govex_id = models.PositiveBigIntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"Profile({self.user})"


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(
        user=user, defaults={"verified": user.is_staff or user.is_superuser}
    )
    return profile


class UserConsent(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consent"
    )
    privacy = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    disclaimer = models.BooleanField(default=False)

    def __str__(self):
        return f"Consent({self.user})"
