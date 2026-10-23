from django.db import migrations


def apply_icons(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")

    try:
        about = SiteContent.objects.get(key="about")
    except SiteContent.DoesNotExist:
        pass
    else:
        changed = False
        for entry in about.data:
            if entry.get("icon") == "switzerland":
                entry["icon"] = "flags/switzerland"
                changed = True
        if changed:
            about.save(update_fields=["data"])

    try:
        cv = SiteContent.objects.get(key="cv")
    except SiteContent.DoesNotExist:
        pass
    else:
        changed = False
        for category in cv.data:
            for item in category.get("items", []):
                if item.get("key") == "military":
                    item["icon"] = "military/medal"
                    changed = True
        if changed:
            cv.save(update_fields=["data"])


def revert_icons(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")

    try:
        about = SiteContent.objects.get(key="about")
    except SiteContent.DoesNotExist:
        pass
    else:
        changed = False
        for entry in about.data:
            if entry.get("icon") == "flags/switzerland":
                entry["icon"] = "switzerland"
                changed = True
        if changed:
            about.save(update_fields=["data"])

    try:
        cv = SiteContent.objects.get(key="cv")
    except SiteContent.DoesNotExist:
        pass
    else:
        changed = False
        for category in cv.data:
            for item in category.get("items", []):
                if item.get("key") == "military":
                    item["icon"] = "flags/switzerland"
                    changed = True
        if changed:
            cv.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0009_legal_section_subtitles"),
    ]

    operations = [
        migrations.RunPython(apply_icons, revert_icons),
    ]
