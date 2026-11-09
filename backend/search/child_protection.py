from datetime import date
from pathlib import Path

from wintersehn.accounts.models import get_or_create_profile

ADULT_AGE = 18
DOMAINS = (Path(__file__).parent / "child_domains.txt").read_text().split()


def age(birthdate, today):
    before_birthday = (today.month, today.day) < (birthdate.month, birthdate.day)
    return today.year - birthdate.year - before_birthday


def is_required(user):
    if not user.is_authenticated:
        return False
    birthdate = get_or_create_profile(user).birthdate
    return bool(birthdate) and age(birthdate, date.today()) < ADULT_AGE


def protect(user, data):
    if not is_required(user):
        return data
    return {**data, "allowlist": DOMAINS, "allowlistEnabled": True}
