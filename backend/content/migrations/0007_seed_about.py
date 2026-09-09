from django.db import migrations

ABOUT = [
    {"label": "Vorname", "value": "Jonas"},
    {"label": "Nachname", "value": "Büchi"},
    {"label": "Geburtsdatum", "value": "6. Januar 2005"},
    {"label": "Nationalität", "value": "Schweiz", "icon": "switzerland"},
    {"label": "Adresse", "value": "CH-3324 Hindelbank, Eichmatt 1"},
]


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="about", defaults={"data": ABOUT})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="about").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0006_alter_sitecontent_options"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
