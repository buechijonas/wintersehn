from django.db import migrations

# The icon library reorganization in f45d91c moved these flat icons out of
# the flats/ root into named subfolders and rewrote the *default* seed data
# in 0002_seed_content.py accordingly, but never shipped a migration to
# update already-seeded "ethos"/"cv" SiteContent rows, so any database
# seeded before that commit is still pointing at the old, now-deleted root
# icon files.
ICON_PATH_FIXES = {
    "galaxy": "physics/galaxy",
    "hieroglyph": "archeology/hieroglyph",
    "sprout": "spring/sprout",
    "videogames": "stay_at_home/videogames",
    "coding": "stem/coding",
    "europe": "europe/europe",
    "music": "stay_at_home/music",
    "mortarboard": "education/graduation_hat",
    "bag": "city_life/bag_2",
    "switzerland": "flags/switzerland",
    "medal": "military/medal",
    "salvation-army": "christmas_characters/salvation_army",
    "politician": "voting_elections/politician",
    "european-union": "flags/european_union",
}


def remap_icons(data, mapping):
    changed = False
    if isinstance(data, dict):
        if data.get("icon") in mapping:
            data["icon"] = mapping[data["icon"]]
            changed = True
        for value in data.values():
            if remap_icons(value, mapping):
                changed = True
    elif isinstance(data, list):
        for item in data:
            if remap_icons(item, mapping):
                changed = True
    return changed


def apply_fixes(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for key in ("ethos", "cv"):
        try:
            content = SiteContent.objects.get(key=key)
        except SiteContent.DoesNotExist:
            continue
        if remap_icons(content.data, ICON_PATH_FIXES):
            content.save(update_fields=["data"])


def revert_fixes(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    reverse_mapping = {new: old for old, new in ICON_PATH_FIXES.items()}
    for key in ("ethos", "cv"):
        try:
            content = SiteContent.objects.get(key=key)
        except SiteContent.DoesNotExist:
            continue
        if remap_icons(content.data, reverse_mapping):
            content.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0010_fix_switzerland_and_military_icons"),
    ]

    operations = [
        migrations.RunPython(apply_fixes, revert_fixes),
    ]
