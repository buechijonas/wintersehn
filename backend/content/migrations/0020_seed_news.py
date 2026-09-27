from django.db import migrations

NEWS = [
    {
        "title": "News",
        "items": [
            {
                "name": "SRF",
                "url": "https://www.srf.ch",
                "category": "Öffentlich-rechtlich",
                "description": "Aktuelle Nachrichten",
            },
            {
                "name": "NZZ",
                "url": "https://www.nzz.ch",
                "category": "Politisch konservativ",
                "description": "Juristische Analysen, Wirtschaftsmagazin",
            },
            {
                "name": "Correctiv",
                "url": "https://correctiv.org",
                "category": "Faktenprüfung",
                "description": "Faktenchecks zu viralen Fake News und Desinformation",
            },
            {
                "name": "Deutsche Welle",
                "url": "https://www.dw.com/de",
                "category": "Politisch liberal",
                "description": "Internationale News, pro-europäisch",
            },
        ],
    },
    {
        "title": "Wissens-News",
        "items": [
            {
                "name": "Quarks",
                "url": "https://www.quarks.de",
                "category": "Sehr empfehlenswert",
                "description": "Wissenschaft, Umwelt, Gesundheit, Gesellschaft, Klima",
            },
            {
                "name": "ARD alpha",
                "url": "https://www.ardalpha.de",
                "category": "Qualitativ hochwertig",
                "description": "Wissenschaft, Bildung",
            },
        ],
    },
    {
        "title": "Tech-News",
        "items": [
            {
                "name": "netzpolitik.org",
                "url": "https://netzpolitik.org",
                "category": "Aktivistisch",
                "description": "Kampf für digitale Freiheit, Überwachungsskandale, Kritik an Big Tech und den USA",
            },
            {
                "name": "Golem",
                "url": "https://www.golem.de",
                "category": "IT-Zeitung",
                "description": "Teilweise schneller als normale Zeitungen",
            },
            {
                "name": "Proton News",
                "url": "https://proton.me/de/blog/news",
                "category": "Werte-Fokus",
                "description": "Datenschutz, digitale Souveränität, Sicherheitsaudits",
            },
            {
                "name": "IT-Magazine.ch",
                "url": "https://www.itmagazine.ch",
                "category": "IT-Fachmagazin",
                "description": "Weniger aktivistisch, mehr marktorientiert, Cybersecurity-Trends",
            },
            {
                "name": "heise online",
                "url": "https://www.heise.de",
                "category": "IT-Portal",
                "description": "Software, Hardware, Open Source, Sicherheit und Digitalpolitik",
            },
        ],
    },
]


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="news", defaults={"data": NEWS})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="news").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0019_cookies_consent"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
