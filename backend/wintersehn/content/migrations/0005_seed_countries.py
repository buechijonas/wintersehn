from django.db import migrations

COUNTRIES = [
    {
        "title": "Wunschliste",
        "items": [
            {"icon": "china", "label": "China", "iconSet": "countries"},
            {"icon": "denmark", "label": "Dänemark", "iconSet": "countries"},
            {"icon": "japan", "label": "Japan", "iconSet": "countries"},
            {"icon": "norway", "label": "Norwegen", "iconSet": "countries"},
            {"icon": "poland", "label": "Polen", "iconSet": "countries"},
            {"icon": "scotland", "label": "Schottland", "iconSet": "countries"},
            {"icon": "sweden", "label": "Schweden", "iconSet": "countries"},
            {"icon": "czech-republic", "label": "Tschechien", "iconSet": "countries"},
            {"icon": "vatican-city", "label": "Vatikanstadt", "iconSet": "countries"},
        ],
    },
    {
        "title": "Bereiste Länder",
        "items": [
            {"icon": "bulgaria", "label": "Bulgarien", "iconSet": "countries"},
            {"icon": "france", "label": "Frankreich", "iconSet": "countries"},
            {"icon": "italy", "label": "Italien", "iconSet": "countries"},
            {"icon": "croatia", "label": "Kroatien", "iconSet": "countries"},
            {"icon": "austria", "label": "Österreich", "iconSet": "countries"},
            {"icon": "switzerland", "label": "Schweiz", "iconSet": "countries"},
        ],
    },
    {
        "title": "Schwarze Liste",
        "items": [
            {"icon": "israel", "label": "Israel", "iconSet": "countries"},
            {"icon": "russia", "label": "Russland", "iconSet": "countries"},
            {"icon": "united-states", "label": "USA", "iconSet": "countries"},
        ],
    },
]


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="countries", defaults={"data": COUNTRIES})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="countries").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_alter_sitecontent_options"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
