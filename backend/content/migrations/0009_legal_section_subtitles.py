from django.db import migrations

LEGAL_KEYS = ["impressum", "privacy", "terms", "disclaimer", "cookies"]


def add_subtitles(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for key in LEGAL_KEYS:
        try:
            content = SiteContent.objects.get(key=key)
        except SiteContent.DoesNotExist:
            continue
        data = content.data
        changed = False
        for section in data.get("sections", []):
            if "subtitle" not in section:
                section["subtitle"] = ""
                changed = True
            if key == "terms" and "items" in section:
                new_items = []
                for item in section["items"]:
                    if "title" in item or "description" in item:
                        new_items.append(
                            {
                                "listtitle": item.get("title", ""),
                                "texttitle": item.get("description", ""),
                            }
                        )
                        changed = True
                    else:
                        new_items.append(item)
                section["items"] = new_items
        if changed:
            content.data = data
            content.save(update_fields=["data"])


def remove_subtitles(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for key in LEGAL_KEYS:
        try:
            content = SiteContent.objects.get(key=key)
        except SiteContent.DoesNotExist:
            continue
        data = content.data
        changed = False
        for section in data.get("sections", []):
            if "subtitle" in section:
                del section["subtitle"]
                changed = True
            if key == "terms" and "items" in section:
                new_items = []
                for item in section["items"]:
                    if "listtitle" in item or "texttitle" in item:
                        new_items.append(
                            {
                                "title": item.get("listtitle", ""),
                                "description": item.get("texttitle", ""),
                            }
                        )
                        changed = True
                    else:
                        new_items.append(item)
                section["items"] = new_items
        if changed:
            content.data = data
            content.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0008_alter_sitecontent_options"),
    ]

    operations = [
        migrations.RunPython(add_subtitles, remove_subtitles),
    ]
