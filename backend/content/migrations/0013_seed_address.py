from django.db import migrations

ADDRESS = {
    "lines": ["Jonas S. Büchi", "Eichmatt 1", "CH-3324 Hindelbank", "Kanton Bern"],
}


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="address", defaults={"data": ADDRESS})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="address").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0012_fold_intro_into_sections"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
