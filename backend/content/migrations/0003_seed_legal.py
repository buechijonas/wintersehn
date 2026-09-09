from django.db import migrations

IMPRESSUM = {
    "title": "Impressum",
    "illustration": "impressum",
    "intro": "Verantwortlich für den Inhalt gemäss §5 TMG (Telemetriegesetz) und Art. 4 Abs. 7 DSGVO",
    "sections": [
        {"address": True},
        {
            "title": "Haftung für Inhalte",
            "text": (
                "Die Inhalte unserer Seite wurden mit grösster Sorgfalt erstellt. Für die Richtigkeit, "
                "Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen."
            ),
        },
        {
            "title": "Obligatorischer Hinweis",
            "text": (
                "Diese Webapplikation gehört Wintersehn. Der Hinweis ist hier aufgrund der geltenden "
                "Impressumspflicht der Europäischen Union und der Schweiz enthalten."
            ),
        },
    ],
}

PRIVACY = {
    "title": "Datenschutzerklärung",
    "breadcrumbLabel": "Datenschutzerklärung",
    "illustration": "privacy",
    "consentField": "privacy",
    "sections": [
        {"title": "1. Verantwortliche Stelle", "address": True},
        {
            "title": "2. Zweck der Datenverarbeitung",
            "text": (
                "Dieses Projekt ist ein rein freizeitliches Vorhaben, das ausschliesslich der "
                "Weiterbildung und Wissensvermittlung dient. Die Nutzung der Webapplikation setzt "
                "voraus, dass die Verarbeitung personenbezogener Daten im Rahmen der Verwaltung durch "
                "mich akzeptiert wird. Nutzer, die dieser Regelung nicht zustimmen möchten, sind "
                "eingeladen, die Plattform nicht weiter zu verwenden."
            ),
        },
        {
            "title": "3. Erhobene Daten",
            "text": (
                "Beim Besuch unserer Webapplikation werden automatisch Informationen durch den "
                "Webserver in sogenannten Log-Dateien gespeichert. Diese beinhalten die IP-Adresse, "
                "den Browsertyp, das Betriebssystem, die Referrer-URL, potenziell Teile des "
                "Browserverlaufs sowie das Datum und die Uhrzeit des Zugriffs. Diese Daten werden "
                "nicht weitergegeben."
            ),
        },
        {
            "title": "4. Rechtsgrundlage",
            "text": (
                "Die Verarbeitung der genannten Daten erfolgt gemäss Art. 6 Abs. 1 lit. f DSGVO, wobei "
                "unser berechtigtes Interesse darin besteht, eine funktionsfähige und "
                "benutzerfreundliche Webapplikation zu betreiben."
            ),
        },
        {
            "title": "5. Dauer der Speicherung",
            "text": (
                "Personenbezogene Daten werden nur so lange gespeichert, wie dies für die Erreichung "
                "der hier genannten Zwecke erforderlich ist, jedoch nach einer Deaktivierung des "
                "Kontos maximal für eine Dauer von 10 Jahren."
            ),
        },
        {
            "title": "6. Weitergabe an Dritte",
            "text": "Es wird versucht, keine personenbezogenen Daten an Dritte weiterzugeben.",
        },
        {
            "title": "7. Rechte der betroffenen Personen",
            "text": (
                "Sie haben das Recht, Auskunft über die von uns verarbeiteten personenbezogenen Daten "
                "zu erhalten, sowie Berichtigung, Löschung oder Einschränkung der Verarbeitung zu "
                "verlangen. Zudem können Sie der Verarbeitung Ihrer personenbezogenen Daten "
                "widersprechen. Bitte wenden Sie sich dazu an die oben angegebene Kontaktadresse."
            ),
        },
        {
            "title": "8. Änderung der Datenschutzerklärung",
            "text": (
                "Wir behalten uns vor, diese Datenschutzerklärung zu ändern, um sie an aktuelle "
                "rechtliche Anforderungen oder Änderungen unserer Leistungen anzupassen. Die jeweils "
                "aktuelle Fassung ist jederzeit auf dieser Webapplikation abrufbar."
            ),
        },
    ],
}

TERMS_ITEMS = [
    ("Antisemitismus", "Jegliche Form von antisemitischer Äusserung oder Handlung."),
    (
        "Ausbeuterische Inhalte",
        "Inhalte, die auf die Ausbeutung von Menschen oder Tieren abzielen.",
    ),
    (
        "Ausweichung von Minderjährigenschutz",
        "Handlungen, die gegen den Schutz von Minderjährigen verstossen, wie z. B. unzulässiger Kontakt.",
    ),
    ("Beleidigung", "Gebrauch von abwertender, beleidigender oder vulgärer Sprache."),
    ("Belohnungsjagd", "Unrechtmässiges Ausnutzen von Funktionen der Plattform."),
    ("Belästigung", "Unangemessene Annäherung, Kontaktaufnahme oder Nachstellung."),
    ("Betrug", "Täuschung oder betrügerisches Verhalten zum Zweck der Bereicherung."),
    (
        "Christophobie",
        "Feindseligkeit oder Vorurteile gegenüber Christen oder dem Christentum.",
    ),
    (
        "Cybergrooming",
        "Versuche, Kinder online zu manipulieren oder zu missbrauchen. Erwachsene, die versuchen, "
        "sich Kindern auf dieser Plattform anzunähern, werden nicht toleriert.",
    ),
    (
        "Diskriminierung",
        "Benachteiligung oder Herabwürdigung von Personen aufgrund von Geschlecht, Rasse, Religion, "
        "sexueller Orientierung oder anderen persönlichen Merkmalen.",
    ),
    (
        "Doxxing",
        "Veröffentlichung oder Weitergabe von privaten Informationen ohne Zustimmung der betroffenen Person.",
    ),
    ("Drohung", "Androhung von Gewalt, Mord oder anderen negativen Konsequenzen."),
    (
        "Erpressung",
        "Jede Handlung, bei der eine Person durch Androhung von Nachteilen zu etwas gezwungen wird.",
    ),
    (
        "Falschinformationen",
        "Verbreitung von falschen oder irreführenden Informationen.",
    ),
    ("Faschismus", "Förderung oder Verbreitung faschistischer Ideologien."),
    (
        "Fremdenfeindlichkeit",
        "Feindseligkeit oder Vorurteile gegenüber Ausländern oder ethnischen Minderheiten.",
    ),
    (
        "Gefährliche Verschwörungstheorien",
        "Verbreitung oder Unterstützung von Theorien, die Panik, Angst oder Gewalt fördern können.",
    ),
    (
        "Gewaltbasierter Inhalt",
        "Verbreitung von Inhalten, die Gewalt fördern oder darstellen.",
    ),
    (
        "Gewaltverherrlichung",
        "Förderung oder Rechtfertigung von Gewalt gegen Einzelpersonen, Gruppen oder Institutionen.",
    ),
    (
        "Hassrede",
        "Äusserungen, die zu Hass oder Gewalt gegen bestimmte Gruppen aufrufen.",
    ),
    ("Homophobie", "Feindseligkeit oder Vorurteile gegenüber homosexuellen Personen."),
    (
        "Identitätsdiebstahl",
        "Falsche Darstellung oder Ausgeben als eine andere Person, Institution oder Entität.",
    ),
    (
        "Illegale Inhalte",
        "Verbreitung oder Bereitstellung von Inhalten, die gegen geltendes Recht verstossen.",
    ),
    (
        "Islamophobie",
        "Feindseligkeit oder Vorurteile gegenüber Muslimen oder dem Islam.",
    ),
    (
        "Kulturelle Aneignung",
        "Unangemessene Nutzung oder Darstellung von kulturellen Symbolen, Traditionen oder Werten.",
    ),
    (
        "Missbrauch von Privilegien",
        "Jegliche Form von ungerechtfertigter Ausnutzung von Rechten oder Zugriffsrechten auf dieser "
        "Webapplikation.",
    ),
    (
        "Plagiate",
        "Hochladen oder Teilen von Inhalten, die ohne Zustimmung von Dritten kopiert oder "
        "vervielfältigt wurden.",
    ),
    (
        "Pornografische Inhalte",
        "Verbreitung, Bereitstellung oder Zugänglichmachung von pornografischen oder sexuellen Inhalten.",
    ),
    (
        "Propaganda",
        "Verbreitung von politisch oder ideologisch einseitigen Informationen zu Manipulationszwecken.",
    ),
    (
        "Rassismus",
        "Diskriminierung oder Feindseligkeit gegenüber Personen aufgrund ihrer ethnischen Herkunft.",
    ),
    (
        "Selbstgefährdung",
        "Inhalte oder Verhaltensweisen, die zu Selbstverletzung oder suizidalem Verhalten ermutigen "
        "oder dieses fördern. Wir bitten darum, stattdessen dazu zu ermutigen, sich Hilfe zu suchen "
        "und mit jemandem darüber zu sprechen.",
    ),
    (
        "Selbstjustiz",
        "Förderung oder Verherrlichung von Handlungen, die darauf abzielen, Recht in die eigene Hand "
        "zu nehmen.",
    ),
    (
        "Sexismus",
        "Diskriminierung oder Herabwürdigung aufgrund des Geschlechts. Das gilt in beide Richtungen, "
        "sowohl Misogynie als auch Misandrie.",
    ),
    (
        "Sextortion",
        "Erpressung unter Androhung, private oder intime Informationen zu veröffentlichen.",
    ),
    (
        "Spam",
        "Unerwünschte und unaufgeforderte Nachrichten, insbesondere Werbenachrichten.",
    ),
    (
        "Unangemessene Wortwahl",
        "Verwendung von respektlosen, beleidigenden oder unangemessenen Ausdrücken.",
    ),
    (
        "Unethische Werbung",
        "Bewerbung von Produkten, Dienstleistungen oder Inhalten, die betrügerisch, unethisch oder "
        "schädlich sind.",
    ),
]

TERMS = {
    "title": "Nutzungsrichtlinien",
    "breadcrumbLabel": "Nutzungsrichtlinien",
    "illustration": "terms",
    "consentField": "terms",
    "sections": [
        {
            "title": "1. Allgemeine Grundsätze",
            "text": (
                "Diese Webapplikation ist ein freizeitliches Vorhaben, das ausschliesslich der "
                "Weiterbildung und Wissensvermittlung dient. Die Nutzung der Webapplikation unterliegt "
                "diesen Nutzungsrichtlinien, die jederzeit von der Verantwortlichen angepasst werden "
                "können. Mit der Nutzung der Webapplikation stimmen Sie diesen Nutzungsrichtlinien zu."
            ),
        },
        {
            "title": "2. Strafrechtliche Verfolgung",
            "text": (
                "Die Nutzung dieser Webapplikation setzt die Einhaltung der geltenden europäischen und "
                "schweizerischen Gesetze voraus. Verstösse wie z. B. Cybermobbing, Datendiebstahl oder "
                "andere rechtswidrige Handlungen werden mit voller Härte strafrechtlich verfolgt. In "
                "solchen Fällen werden sämtliche personenbezogenen und hochsensiblen Daten an die "
                "zuständigen Behörden weitergeleitet, um die Verfolgung und Ahndung solcher Straftaten "
                "sicherzustellen."
            ),
        },
        {
            "title": "3. Verhaltensregeln",
            "text": (
                "Um eine sichere und respektvolle Umgebung für alle Benutzer zu gewährleisten, sind "
                "die folgenden Verhaltensweisen auf dieser Webapplikation strengstens untersagt:"
            ),
            "items": [
                {"title": title, "description": description}
                for title, description in TERMS_ITEMS
            ],
        },
        {
            "title": "4. Änderung der Nutzungsrichtlinien",
            "text": (
                "Die Nutzungsrichtlinien können jederzeit ohne vorherige Ankündigung geändert werden. "
                "Nutzer werden gebeten, die Richtlinien regelmässig zu überprüfen, um auf dem neusten "
                "Stand zu bleiben."
            ),
        },
        {
            "title": "5. Geistiges Eigentum",
            "text": (
                "Alle Inhalte auf dieser Plattform, einschliesslich Texte, Bilder, Grafiken, Logos und "
                "Software, sind urheberrechtlich geschützt. Die Vervielfältigung, Verbreitung oder "
                "Verwendung der Inhalte ohne ausdrückliche Genehmigung ist untersagt."
            ),
        },
        {
            "title": "6. Missbrauchsmeldung",
            "text": (
                "Wenn Sie Verstösse gegen die Nutzungsrichtlinien oder missbräuchliches Verhalten "
                "feststellen, sind Sie verpflichtet, dies unverzüglich über die vorgesehenen Meldewege "
                "zu melden. Sollte dies nicht geschehen, verstossen Sie gegen die Nutzungsrichtlinien."
            ),
        },
    ],
}

DISCLAIMER = {
    "title": "Haftungsausschluss",
    "breadcrumbLabel": "Haftungsausschluss",
    "illustration": "disclaimer",
    "consentField": "disclaimer",
    "sections": [
        {
            "title": "1. Inhalt des Onlineangebots",
            "text": (
                "Die Inhalte dieser Webapplikation wurden mit grösstmöglicher Sorgfalt entwickelt. Für "
                "die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine "
                "Gewähr übernehmen. Als Dienstanbieter sind wir gemäss § 7 Abs. 1 TMG für eigene "
                "Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach § 8 bis "
                "10 TMG sind wir jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde "
                "Informationen zu überwachen oder nach Umständen zu forschen, die auf eine "
                "rechtswidrige Tätigkeit hinweisen, wenn sie sich auf einer externen Plattform "
                "befinden. Verpflichtungen zur Entfernung oder Sperrung der Nutzung von uns erstellten "
                "Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine "
                "diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten "
                "Rechtsverletzung möglich. Bei Bekanntwerden von entsprechenden Rechtsverletzungen "
                "werden wir diese Inhalte umgehend entfernen."
            ),
        },
        {
            "title": "2. Haftung für Links",
            "text": (
                "Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir "
                "keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr "
                "übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter "
                "oder Betreiber der Seiten verantwortlich. Eine permanente inhaltliche Kontrolle der "
                "verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht "
                "zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend "
                "entfernen."
            ),
        },
        {
            "title": "3. Urheberrecht",
            "text": (
                "Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten "
                "unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung "
                "und jede Art von Verwertung ausserhalb der Grenzen des Urheberrechts bedürfen der "
                "schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien "
                "dieser Seiten sind nur für den privaten Gebrauch gestattet. Soweit die Inhalte auf "
                "dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte Dritter "
                "beachtet, insbesondere werden Inhalte Dritter als solche gekennzeichnet. Sollten Sie "
                "trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen "
                "entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige "
                "Inhalte umgehend entfernen."
            ),
        },
        {
            "title": "4. Haftung für Schäden",
            "text": (
                "Wir schliessen jegliche Haftung für Schäden aus, die direkt oder indirekt aus der "
                "Nutzung dieser Webapplikation und der darin enthaltenen Informationen entstehen, "
                "soweit diese nicht auf Vorsatz oder grober Fahrlässigkeit beruhen."
            ),
        },
        {
            "title": "5. Keine Abmahnung ohne vorherigen Kontakt",
            "text": (
                "Sollten Inhalte dieser Webapplikation die Rechte Dritter oder gesetzliche "
                "Bestimmungen verletzen, bitten wir um eine entsprechende Nachricht ohne Kostennote. "
                "Wir garantieren, dass die zu Recht beanstandeten Inhalte analysiert und evaluiert "
                "werden, ohne dass die Einschaltung eines Rechtsbeistandes erforderlich ist. Dennoch "
                "von Ihnen ohne vorherige Kontaktaufnahme ausgelöste Kosten werden wir vollständig "
                "zurückweisen und gegebenenfalls Gegenklage wegen Verletzung vorgenannter Bestimmungen "
                "erheben."
            ),
        },
    ],
}

COOKIES = {
    "title": "Cookierichtlinie",
    "breadcrumbLabel": "Cookierichtlinie",
    "sections": [
        {
            "title": "1. Was sind Cookies?",
            "text": (
                "Cookies sind kleine Textdateien, die beim Besuch einer Webapplikation auf Ihrem Gerät "
                "gespeichert werden."
            ),
        },
        {
            "title": "2. Welche Cookies verwenden wir?",
            "text": (
                "Diese Webapplikation verwendet ausschliesslich technisch notwendige Cookies (Session- "
                "und Sicherheits-Cookies), um die Anmeldung und den Schutz vor Cross-Site-Request-"
                "Forgery zu ermöglichen. Es werden keine Tracking-, Marketing- oder Analyse-Cookies "
                "eingesetzt."
            ),
        },
        {
            "title": "3. Verwaltung von Cookies",
            "text": (
                "Sie können die Speicherung von Cookies in Ihrem Browser jederzeit deaktivieren. Da "
                "die verwendeten Cookies für die Anmeldefunktion technisch notwendig sind, ist die "
                "Nutzung geschützter Bereiche ohne sie eingeschränkt."
            ),
        },
    ],
}


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for key, data in [
        ("impressum", IMPRESSUM),
        ("privacy", PRIVACY),
        ("terms", TERMS),
        ("disclaimer", DISCLAIMER),
        ("cookies", COOKIES),
    ]:
        SiteContent.objects.get_or_create(key=key, defaults={"data": data})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(
        key__in=["impressum", "privacy", "terms", "disclaimer", "cookies"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0002_seed_content"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
