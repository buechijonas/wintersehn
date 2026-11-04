from django.db import migrations

APPS = [
    {
        "title": "Ersetzt",
        "items": [
            {
                "name": "Linux Bazzite",
                "icon": "bazzite",
                "footprint": 2,
                "url": "https://bazzite.gg",
                "category": "Betriebssystem",
                "replaces": [
                    {
                        "name": "Windows",
                        "icon": "windows",
                        "country": "united_states",
                        "footprint": 8,
                    }
                ],
                "reason": "Gaming läuft dank Steam und Proton problemlos, ganz ohne Telemetrie und Zwangs-Updates.",
            },
            {
                "name": "Fairphone mit /e/OS",
                "icon": "eos",
                "country": "france",
                "footprint": 2,
                "url": "https://e.foundation",
                "category": "Smartphone",
                "replaces": [
                    {
                        "name": "iPhone mit iOS",
                        "icon": "apple",
                        "country": "united_states",
                        "footprint": 6,
                    }
                ],
                "reason": "Android ohne Google-Dienste auf einem reparierbaren, fair produzierten Smartphone.",
            },
            {
                "name": "Brave",
                "icon": "brave",
                "country": "united_states",
                "footprint": 2,
                "url": "https://brave.com",
                "category": "Browser",
                "description": "Mobil",
                "replaces": [
                    {
                        "name": "Safari",
                        "icon": "safari",
                        "country": "united_states",
                        "footprint": 4,
                    }
                ],
                "reason": "Blockiert Werbung und Tracker standardmässig, auch auf dem Handy.",
            },
            {
                "name": "Brave",
                "icon": "brave",
                "country": "united_states",
                "footprint": 2,
                "url": "https://brave.com",
                "category": "Browser",
                "description": "Desktop",
                "replaces": [
                    {
                        "name": "Chrome",
                        "icon": "googlechrome",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "Volle Chromium-Kompatibilität, aber ohne Googles Datensammlung.",
            },
            {
                "name": "Startpage",
                "icon": "startpage",
                "country": "netherlands",
                "footprint": 2,
                "url": "https://www.startpage.com",
                "category": "Suchmaschine",
                "replaces": [
                    {
                        "name": "Google",
                        "icon": "google",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "Liefert Google-Suchergebnisse, ohne mein Suchverhalten zu speichern oder ein Profil anzulegen.",
            },
            {
                "name": "Threema",
                "icon": "threema",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://threema.ch",
                "category": "Messenger",
                "replaces": [
                    {
                        "name": "WhatsApp",
                        "icon": "whatsapp",
                        "country": "united_states",
                        "footprint": 7,
                    }
                ],
                "reason": "Schweizer Messenger, Ende-zu-Ende-verschlüsselt und ohne Telefonnummer nutzbar.",
            },
            {
                "name": "Proton Mail",
                "icon": "protonmail",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://proton.me/mail",
                "category": "E-Mail",
                "replaces": [
                    {
                        "name": "Gmail",
                        "icon": "gmail",
                        "country": "united_states",
                        "footprint": 8,
                    }
                ],
                "reason": "Verschlüsselte E-Mails aus der Schweiz, ohne dass meine Inhalte für Werbung ausgewertet werden.",
            },
            {
                "name": "Proton Drive",
                "icon": "protondrive",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://proton.me/drive",
                "category": "Cloud-Speicher",
                "replaces": [
                    {
                        "name": "OneDrive",
                        "icon": "onedrive",
                        "country": "united_states",
                        "footprint": 6,
                    }
                ],
                "reason": "Verschlüsselter Cloud-Speicher in der Schweiz statt bei einem US-Konzern.",
            },
            {
                "name": "Lumo",
                "icon": "lumo",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://lumo.proton.me",
                "category": "KI-Assistent",
                "replaces": [
                    {
                        "name": "ChatGPT",
                        "icon": "chatgpt",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "KI-Assistent von Proton ohne Chat-Protokolle. Gespräche werden verschlüsselt gespeichert und nicht zum Training verwendet.",
            },
            {
                "name": "swissfy",
                "icon": "swissfy",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://swissfy.ch",
                "category": "Social Media",
                "replaces": [
                    {
                        "name": "Instagram",
                        "icon": "instagram",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "Mein eigenes soziales Netzwerk, in dem Chats Ende-zu-Ende-verschlüsselt sind und Beiträge verschlüsselt gespeichert werden.",
            },
            {
                "name": "Qobuz",
                "icon": "qobuz",
                "country": "france",
                "footprint": 3,
                "url": "https://www.qobuz.com",
                "category": "Musik",
                "replaces": [
                    {
                        "name": "Spotify",
                        "icon": "spotify",
                        "country": "sweden",
                        "footprint": 6,
                    }
                ],
                "reason": "Musik in Hi-Res-Qualität und eine fairere Vergütung für Künstlerinnen und Künstler.",
            },
            {
                "name": "Organic Maps",
                "icon": "organicmaps",
                "country": "estonia",
                "footprint": 1,
                "url": "https://organicmaps.app",
                "category": "Navigation",
                "replaces": [
                    {
                        "name": "Google Maps",
                        "icon": "googlemaps",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "Offline-Karten auf Basis von OpenStreetMap, ganz ohne Standort-Tracking.",
            },
            {
                "name": "LibreTube",
                "icon": "libretube",
                "footprint": 1,
                "url": "https://libretube.dev",
                "category": "Video",
                "description": "Mobil",
                "replaces": [
                    {
                        "name": "YouTube",
                        "icon": "youtube",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "YouTube ohne Werbung, Tracking und Google-Konto auf dem Handy.",
            },
            {
                "name": "FreeTube",
                "icon": "freetube",
                "footprint": 1,
                "url": "https://freetubeapp.io",
                "category": "Video",
                "description": "Desktop",
                "replaces": [
                    {
                        "name": "YouTube",
                        "icon": "youtube",
                        "country": "united_states",
                        "footprint": 9,
                    }
                ],
                "reason": "YouTube am Desktop ohne Werbung und Tracking, meine Abos bleiben lokal gespeichert.",
            },
            {
                "name": "LibreOffice Writer",
                "icon": "libreofficewriter",
                "country": "germany",
                "footprint": 1,
                "url": "https://de.libreoffice.org",
                "category": "Textverarbeitung",
                "replaces": [
                    {
                        "name": "Microsoft Word",
                        "icon": "msword",
                        "country": "united_states",
                        "footprint": 6,
                    }
                ],
                "reason": "Freie Textverarbeitung ohne Cloud-Zwang und Telemetrie, gespeichert im offenen ODF-Format.",
            },
            {
                "name": "LibreOffice Impress",
                "icon": "libreofficeimpress",
                "country": "germany",
                "footprint": 1,
                "url": "https://de.libreoffice.org",
                "category": "Präsentation",
                "replaces": [
                    {
                        "name": "Microsoft PowerPoint",
                        "icon": "mspowerpoint",
                        "country": "united_states",
                        "footprint": 6,
                    }
                ],
                "reason": "Präsentationen bleiben lokal auf meinem Gerät statt automatisch in der Microsoft-Cloud.",
            },
            {
                "name": "LibreOffice Calc",
                "icon": "libreofficecalc",
                "country": "germany",
                "footprint": 1,
                "url": "https://de.libreoffice.org",
                "category": "Tabellenkalkulation",
                "replaces": [
                    {
                        "name": "Microsoft Excel",
                        "icon": "msexcel",
                        "country": "united_states",
                        "footprint": 6,
                    }
                ],
                "reason": "Tabellen ohne Microsoft-Konto und Datensammlung, quelloffen und kostenlos.",
            },
        ],
    },
    {
        "title": "Verzichtet",
        "items": [
            {
                "name": "Threads",
                "category": "Microblogging",
                "icon": "threads",
                "country": "united_states",
                "footprint": 9,
                "dropped": True,
                "reason": "Gehört wie Instagram zu Meta und sammelt entsprechend viele Daten.",
            },
            {
                "name": "TikTok",
                "category": "Kurzvideos",
                "icon": "tiktok",
                "country": "china",
                "footprint": 10,
                "dropped": True,
                "reason": "Suchtfördernder Algorithmus und ein intransparenter Umgang mit Nutzerdaten.",
            },
            {
                "name": "X",
                "category": "Microblogging",
                "icon": "x",
                "country": "united_states",
                "footprint": 8,
                "dropped": True,
                "reason": "Seit der Übernahme mehr Desinformation und deutlich weniger Moderation.",
            },
        ],
    },
    {
        "title": "Sicherheit (empfohlen)",
        "items": [
            {
                "name": "1Password",
                "icon": "1password",
                "country": "canada",
                "footprint": 2,
                "url": "https://1password.com",
                "category": "Passwort-Manager",
                "reason": "Ein starkes, einzigartiges Passwort für jeden Dienst, sicher auf allen Geräten.",
            },
            {
                "name": "YubiKey",
                "icon": "yubico",
                "country": "sweden",
                "footprint": 1,
                "url": "https://www.yubico.com",
                "category": "MFA",
                "reason": "Ein Hardware-Schlüssel als zweiter Faktor, der zuverlässig vor Phishing schützt.",
            },
            {
                "name": "Passmails",
                "icon": "protonpass",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://proton.me/pass",
                "category": "E-Mail-Aliase",
                "reason": "Für jeden Dienst eine eigene Adresse. So bleibt meine echte E-Mail privat und Spam lässt sich abschalten.",
            },
            {
                "name": "Proton VPN",
                "icon": "protonvpn",
                "country": "switzerland",
                "footprint": 1,
                "url": "https://protonvpn.com",
                "category": "VPN",
                "reason": "Schützt meine Verbindung in öffentlichen WLANs, mit geprüfter No-Log-Policy aus der Schweiz.",
            },
        ],
        "separate": True,
    },
    {
        "title": "Nächste Schritte",
        "items": [
            {
                "name": "Motorola mit GrapheneOS",
                "icon": "grapheneos",
                "country": "canada",
                "footprint": 1,
                "url": "https://grapheneos.org",
                "category": "Smartphone",
                "planned": True,
                "replaces": [
                    {
                        "name": "Fairphone mit /e/OS",
                        "icon": "eos",
                        "country": "france",
                        "footprint": 2,
                    }
                ],
                "reason": "Gehärtetes Android ohne Google-Dienste, das vor forensischer Auswertung schützt. Ein Auto-Neustart verschlüsselt das Gerät nach Inaktivität wieder, USB-Daten bleiben im gesperrten Zustand blockiert und eine Notfall-PIN löscht alle Daten unwiderruflich.",
            },
            {
                "name": "Mullvad Browser",
                "icon": "mullvad",
                "country": "sweden",
                "footprint": 1,
                "url": "https://mullvad.net/de/browser",
                "category": "Browser",
                "description": "Desktop",
                "planned": True,
                "replaces": [
                    {
                        "name": "Brave",
                        "icon": "brave",
                        "country": "united_states",
                        "footprint": 2,
                    }
                ],
                "reason": "Basiert auf dem Tor Browser. Alle Nutzer sehen gleich aus, was Fingerprinting verhindert, und Verlauf sowie Cookies werden beim Schliessen gelöscht.",
            },
            {
                "name": "SearXNG",
                "icon": "searxng",
                "footprint": 1,
                "url": "https://docs.searxng.org",
                "category": "Suchmaschine",
                "description": "Selbst gehostet",
                "planned": True,
                "replaces": [
                    {
                        "name": "Startpage",
                        "icon": "startpage",
                        "country": "netherlands",
                        "footprint": 2,
                    }
                ],
                "reason": "Meta-Suchmaschine auf meinem eigenen Server. Suchanfragen laufen über viele Quellen, ohne Profil und ohne fremden Betreiber dazwischen.",
            },
            {
                "name": "Penpot",
                "icon": "penpot",
                "country": "spain",
                "footprint": 1,
                "url": "https://penpot.app",
                "category": "Design",
                "planned": True,
                "replaces": [
                    {
                        "name": "Figma",
                        "icon": "figma",
                        "country": "united_states",
                        "footprint": 6,
                    }
                ],
                "reason": "Quelloffenes Designtool, das sich selbst hosten lässt. Meine Entwürfe liegen auf meinem Server statt in der Figma-Cloud.",
            },
            {
                "name": "Pi-hole",
                "icon": "pihole",
                "footprint": 1,
                "url": "https://pi-hole.net",
                "category": "Netzwerk-Werbeblocker",
                "planned": True,
                "reason": "Blockiert Werbung und Tracker für alle Geräte im Heimnetz direkt auf DNS-Ebene, auch auf Smart-TVs und in Apps ohne eigenen Blocker.",
            },
        ],
        "separate": True,
    },
]

NEWS_ICONS = {
    "SRF": "srf",
    "NZZ": "nzz",
    "Correctiv": "correctiv",
    "Deutsche Welle": "dw",
    "Quarks": "quarks",
    "ARD alpha": "ardalpha",
    "netzpolitik.org": "netzpolitik",
    "Golem": "golem",
    "Proton News": "proton",
    "heise online": "heise",
}


def news_card(item):
    card = {
        "name": item["name"],
        "url": item["url"],
        "category": item["category"],
        "reason": item["description"],
    }
    if item["name"] in NEWS_ICONS:
        card["icon"] = NEWS_ICONS[item["name"]]
    return card


def news_item(card):
    return {
        "name": card["name"],
        "url": card["url"],
        "category": card["category"],
        "description": card["reason"],
    }


def split_sections(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    try:
        content = SiteContent.objects.get(key="news")
    except SiteContent.DoesNotExist:
        return
    content.data = [
        {
            "title": "Medien",
            "items": [
                {
                    "key": "news",
                    "icon": "breakfast/047-newspaper",
                    "label": "Nachrichten",
                    "to": "/news/news",
                    "description": "Die Medien, denen ich vertraue und die ich regelmässig konsumiere.",
                    "groups": [
                        {**group, "items": [news_card(item) for item in group["items"]]}
                        for group in content.data
                    ],
                },
                {
                    "key": "apps",
                    "icon": "creative_web/mobile_app",
                    "label": "Apps & Software",
                    "to": "/news/apps",
                    "description": "Meine Massnahmen gegen Massenüberwachung. Ich verkleinere meinen digitalen Fussabdruck, indem ich Dienste grosser Datenkonzerne durch datensparsame Alternativen ersetze, wenn möglich aus der Schweiz und Europa.",
                    "privacy": {
                        "title": "Privacy-Faktor",
                        "description": "Wohin meine Daten fliessen, ist entscheidend. US-Konzerne unterliegen dem CLOUD Act und FISA Section 702. Damit dürfen US-Behörden auf ihre Daten zugreifen, auch wenn diese in Europa gespeichert sind, und Nicht-Amerikaner geniessen dabei kaum Schutz. Spätestens seit den Snowden-Enthüllungen zu PRISM ist klar, dass diese Massenüberwachung real ist.",
                    },
                    "groups": APPS,
                },
            ],
        }
    ]
    content.save(update_fields=["data"])


def merge_sections(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    try:
        content = SiteContent.objects.get(key="news")
    except SiteContent.DoesNotExist:
        return
    sections = content.data[0]["items"]
    groups = next(section["groups"] for section in sections if section["key"] == "news")
    content.data = [
        {**group, "items": [news_item(card) for card in group["items"]]}
        for group in groups
    ]
    content.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0022_destination"),
    ]

    operations = [
        migrations.RunPython(split_sections, merge_sections),
    ]
