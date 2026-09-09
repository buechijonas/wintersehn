from django.db import migrations

ETHOS = [
    {
        "title": "Interessen",
        "items": [
            {"icon": "galaxy", "label": "Astronomie"},
            {"icon": "computer-science", "label": "Informatik"},
            {"icon": "geopolitics", "label": "Geopolitik"},
            {"icon": "hieroglyph", "label": "Geschichte"},
            {"icon": "sprout", "label": "Umwelt & Klima"},
        ],
    },
    {
        "title": "Hobbys",
        "items": [
            {"icon": "videogames", "label": "Gaming"},
            {"icon": "terraria", "label": "Terrarium"},
            {"icon": "coding", "label": "Programmieren"},
            {"icon": "web-design", "label": "Web design"},
            {"icon": "europe", "label": "Propaganda"},
        ],
    },
    {
        "title": "Aktivitäten",
        "items": [
            {"icon": "music", "label": "Klavier"},
            {"icon": "photo-excursion", "label": "Fotoexkursion"},
            {"icon": "hiking", "label": "Wandern"},
            {"icon": "ski", "label": "Ski"},
        ],
    },
]

CV = [
    {
        "title": "Werdegang",
        "items": [
            {
                "key": "academic",
                "icon": "mortarboard",
                "label": "Akademischer Werdegang",
                "to": "/cv/academic",
                "timeline": [
                    {
                        "year": "2025",
                        "title": "Berufsmatura",
                        "description": "Gibb BMS",
                        "side": "start",
                    },
                    {
                        "year": "2021",
                        "title": "Berufsschule",
                        "description": "Gibb IET",
                        "side": "end",
                    },
                    {
                        "year": "2018",
                        "title": "Oberstufe",
                        "description": "Sek E",
                        "side": "start",
                    },
                    {
                        "year": "2017",
                        "title": "Oberstufe",
                        "description": "Sek B",
                        "side": "end",
                    },
                    {
                        "year": "2014",
                        "title": "Mittelstufe",
                        "description": "4. bis 6. Klasse",
                        "side": "start",
                    },
                ],
            },
            {
                "key": "professional",
                "icon": "bag",
                "label": "Beruflicher Werdegang",
                "to": "/cv/professional",
                "timeline": [
                    {
                        "year": "2025",
                        "title": "histify AG",
                        "description": "Jr. Software Engineer",
                        "icon": "histify",
                        "side": "start",
                    },
                    {
                        "year": "2024",
                        "title": "histify AG",
                        "description": "Informatiker EFZ",
                        "icon": "histify",
                        "side": "end",
                        "links": [
                            {
                                "label": "Fähigkeitszeugnis",
                                "url": "https://drive.proton.me/urls/08XA13R08M#w8uFE9LgGKwZ",
                            },
                            {
                                "label": "Kompetenznachweis",
                                "url": "https://drive.proton.me/urls/N0DF9798RC#DMMps3CMq7e2",
                            },
                            {
                                "label": "Abschlussarbeit",
                                "url": "https://drive.proton.me/urls/R9RM8S2WMM#WwQdbe8wGppK",
                            },
                        ],
                    },
                    {
                        "year": "2021",
                        "title": "4teamwork AG",
                        "description": "Informatiker EFZ",
                        "icon": "4tw",
                        "side": "start",
                    },
                ],
            },
            {
                "key": "military",
                "icon": "switzerland",
                "label": "Militärischer Werdegang",
                "to": "/cv/military",
                "timeline": [
                    {
                        "year": "2027",
                        "title": "Schweizer Armee",
                        "description": "Funkaufklärer",
                        "icon": "medal",
                        "side": "start",
                    },
                ],
            },
            {
                "key": "nonprofit",
                "icon": "salvation-army",
                "label": "Gemeinnütziger Werdegang",
                "to": "/cv/nonprofit",
                "timeline": [
                    {
                        "year": "2024",
                        "title": "Heilsarmee",
                        "description": "Technik Gottesdienst",
                        "side": "start",
                    },
                ],
            },
            {
                "key": "political",
                "icon": "politician",
                "label": "Politischer Werdegang",
                "to": "/cv/political",
                "timeline": [
                    {
                        "year": "2025",
                        "title": "We are Europe",
                        "description": "Euro-Föderalist",
                        "icon": "european-union",
                        "side": "start",
                    },
                ],
            },
        ],
    },
]

MEDIA = [
    {
        "title": "Gaming",
        "items": [
            {
                "platform": "Discord",
                "icon": "discord",
                "name": "Wintersehn",
                "url": "https://discord.com/",
            },
            {
                "platform": "Steam",
                "icon": "steam",
                "name": "Wintersehn",
                "url": "https://steamcommunity.com/id/wintersehn/",
            },
            {
                "platform": "Epic Games",
                "icon": "epicgames",
                "name": "Wintersehn",
                "url": "https://epicgames.com/",
            },
            {
                "platform": "Minecraft",
                "icon": "minecraft",
                "name": "Wintersehn",
                "url": "https://www.minecraft.net/",
            },
        ],
    },
    {
        "title": "Arbeit",
        "requiresAuth": True,
        "items": [
            {
                "platform": "LinkedIn",
                "icon": "linkedin",
                "name": "Jonas S. Büchi",
                "url": "https://www.linkedin.com/in/buechijonas/",
            },
            {
                "platform": "GitHub",
                "icon": "github",
                "name": "buechijonas",
                "url": "https://github.com/buechijonas",
            },
            {
                "platform": "histify AG",
                "icon": "histify",
                "name": "histify AG",
                "url": "https://histify.com/",
            },
        ],
    },
    {
        "title": "Kontakt",
        "items": [
            {
                "platform": "Proton Mail",
                "icon": "protonmail",
                "name": "contact@wintersehn.ch",
                "url": "mailto:contact@wintersehn.ch",
            },
        ],
    },
]


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for key, data in [("ethos", ETHOS), ("cv", CV), ("media", MEDIA)]:
        SiteContent.objects.get_or_create(key=key, defaults={"data": data})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key__in=["ethos", "cv", "media"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
