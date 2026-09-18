from django.db import migrations


def fold_intro(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    try:
        content = SiteContent.objects.get(key="impressum")
    except SiteContent.DoesNotExist:
        return
    data = content.data
    intro = data.pop("intro", None)
    if intro is None:
        return
    data["sections"] = [
        {"title": "", "subtitle": "", "text": intro, "items": []},
        *data.get("sections", []),
    ]
    content.data = data
    content.save(update_fields=["data"])


def unfold_intro(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    try:
        content = SiteContent.objects.get(key="impressum")
    except SiteContent.DoesNotExist:
        return
    data = content.data
    sections = data.get("sections", [])
    if not sections:
        return
    first = sections[0]
    if first.get("title") or first.get("subtitle") or first.get("items") or not first.get("text"):
        return
    data["intro"] = first["text"]
    data["sections"] = sections[1:]
    content.data = data
    content.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0011_fix_pre_reorg_ethos_cv_icons"),
    ]

    operations = [
        migrations.RunPython(fold_intro, unfold_intro),
    ]
