from django.db import migrations


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="article", defaults={"data": []})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="article").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0013_seed_address"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
