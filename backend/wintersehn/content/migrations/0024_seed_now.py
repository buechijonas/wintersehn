from django.db import migrations


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="now", defaults={"data": []})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="now").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0023_split_news_sections"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
