from django.db import migrations

SERIALIZER = """class BaseModelSerializer:
    list = None
    retrieve = None

    @classmethod
    def for_action(cls, action):
        if action == "list":
            return cls.list or cls.read
        if action in READ_ACTIONS:
            return cls.retrieve or cls.read
        return cls.write"""

ACL = """class AdminQuerySet(BaseQuerySet):
    def apply_acl(self, user):
        if user.has_perm("content.view_admin"):
            return self
        return self.none()


def get_queryset(self):
    return Exam.objects.apply_acl(self.request.user).detailed()"""

BLIND_INDEX = """class HashField(models.CharField):
    def pre_save(self, model_instance, add):
        value = model_instance.serializable_value(self.source)
        return blind_index(value)


tag_hash = HashField("tag")
Trait.objects.filter(tag_hash__in=blind_indexes(tags))"""

LOOKALIKE = """def scripts(label):
    return {
        unicodedata.name(char, "UNKNOWN").split(" ")[0]
        for char in label
        if char.isalpha()
    }


def is_lookalike(label):
    if label is None:
        return True
    found = scripts(label)
    return len(found) > 1 or bool(found & CONFUSABLE_SCRIPTS)"""

UPLOAD = """def append(self, stream, offset):
    if offset != self.received:
        raise UploadError("Unerwartete Position im Upload.")
    with self.partial.open("ab") as target:
        while chunk := stream.read(1024 * 1024):
            self.received += len(chunk)
            if self.received > self.size:
                raise UploadError("Die Datei ist grösser als angekündigt.")
            target.write(chunk)
    self.save(update_fields=["received"])"""

REPULSION = """const push = (strength * alpha) / Math.max(dx * dx + dy * dy, 100)
a.vx -= dx * push
a.vy -= dy * push
b.vx += dx * push
b.vy += dy * push

const missing = minimumLength(link) - length
if (missing <= 0) return
const shift = missing / length / 2
source.x -= dx * shift
target.x += dx * shift"""

UNTANGLE = """function side(p, q, r) {
  return Math.sign((q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x))
}

function crosses({ source: a, target: b }, { source: c, target: d }) {
  if (new Set([a, b, c, d]).size < 4) return false
  return side(a, b, c) !== side(a, b, d) && side(c, d, a) !== side(c, d, b)
}

const t = Math.max(
  0,
  Math.min(1, ((node.x - source.x) * lx + (node.y - source.y) * ly) / (lx * lx + ly * ly || 1)),
)"""

ZOOM = """zoomAt(factor, clientX, clientY) {
  const k = Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, this.view.k * factor))
  const svg = this.$refs.viewport.ownerSVGElement
  const origin = new DOMPoint(clientX, clientY).matrixTransform(svg.getScreenCTM().inverse())
  const ratio = k / this.view.k
  this.view = {
    k,
    x: origin.x - (origin.x - this.view.x) * ratio,
    y: origin.y - (origin.y - this.view.y) * ratio,
  }
},
wheel(event) {
  this.zoomAt(Math.exp(-event.deltaY / 500), event.clientX, event.clientY)
},"""

CIRCLES = """place(level, index, count) {
  const angle = -Math.PI / 2 + ((index + 0.5) / count) * 2 * Math.PI
  const radius = this.orbit(level)
  return { x: radius * Math.cos(angle), y: radius * Math.sin(angle) }
},
levelAt({ x, y }) {
  const band = Math.ceil((Math.hypot(x, y) - CORE) / BAND)
  return band > this.levels ? null : Math.max(1, band)
},"""

DIGEST = """def blind_digest(data):
    if not settings.MONOLITH_HASH_KEY:
        raise ImproperlyConfigured("MONOLITH_HASH_KEY must be set.")
    key = settings.MONOLITH_HASH_KEY.encode()
    return hmac.new(key, data, hashlib.sha256).hexdigest()"""

REPOSITORY = "https://github.com/buechijonas/wintersehn/blob/main/"

SITES = {
    "wintersehn": {
        "label": "wintersehn.ch",
        "url": "https://wintersehn.ch",
        "public": True,
    },
    "search": {
        "label": "search.wintersehn.ch",
        "url": "https://search.wintersehn.ch",
        "public": True,
    },
    "home": {
        "label": "home.wintersehn.ch",
        "url": "https://home.wintersehn.ch",
        "public": False,
    },
    "atlas": {
        "label": "atlas.wintersehn.ch",
        "url": "https://atlas.wintersehn.ch",
        "public": False,
    },
    "lumon": {
        "label": "lumon.wintersehn.ch",
        "url": "https://lumon.wintersehn.ch",
        "public": False,
    },
    "monolith": {
        "label": "monolith.wintersehn.ch",
        "url": "https://monolith.wintersehn.ch",
        "public": False,
    },
}
ALL_SITES = list(SITES.values())

ENGINEERING = [
    {
        "kind": "intro",
        "title": "Engineering",
        "text": (
            "Wintersehn ist selbst gebaut und selbst betrieben: sechs Web-Apps, "
            "ein gemeinsames Backend und ein einzelner Server mit 1 GB Arbeitsspeicher. "
            "Hier ein Blick hinter die Kulissen."
        ),
        "link": {
            "label": "Projekt auf GitHub",
            "url": "https://github.com/buechijonas/wintersehn",
        },
    },
    {
        "kind": "group",
        "title": "Plattform",
        "text": "Was alle Apps teilen: Server, Backend, Anmeldung und Betrieb.",
        "sites": ALL_SITES,
    },
    {
        "kind": "diagram",
        "title": "Systemübersicht",
        "text": "Jede Anfrage durchläuft dieselben Stationen, über Tor ohne den Bot-Schutz dazwischen.",
        "columns": [
            {
                "title": "Clients",
                "nodes": [
                    {"id": "browser", "label": "Browser"},
                    {"id": "tor-browser", "label": "Tor-Browser"},
                ],
            },
            {
                "title": "Eingang",
                "nodes": [
                    {"id": "edge", "label": "Caddy Edge", "note": "TLS, Header"},
                    {"id": "onion", "label": "Onion-Dienst"},
                ],
            },
            {
                "title": "Schutz",
                "nodes": [{"id": "anubis", "label": "Anubis", "note": "Bot-Schutz"}],
            },
            {
                "title": "Auslieferung",
                "nodes": [
                    {"id": "origin", "label": "Caddy Origin", "note": "Frontends, CSP"}
                ],
            },
            {
                "title": "Dienste",
                "nodes": [
                    {"id": "backend", "label": "Django", "note": "REST-API"},
                    {"id": "searxng", "label": "SearXNG", "note": "Metasuche"},
                ],
            },
            {
                "title": "Grundlage",
                "nodes": [
                    {"id": "postgres", "label": "PostgreSQL", "note": "verschlüsselt"},
                    {"id": "tor", "label": "Tor", "note": "3 Instanzen"},
                ],
            },
        ],
        "edges": [
            ["browser", "edge"],
            ["tor-browser", "onion"],
            ["edge", "anubis"],
            ["anubis", "origin"],
            ["onion", "origin"],
            ["origin", "backend"],
            ["origin", "searxng"],
            ["backend", "postgres"],
            ["searxng", "tor"],
        ],
    },
    {
        "kind": "stack",
        "title": "Technologien",
        "groups": [
            {
                "title": "Frontend",
                "items": [
                    {"name": "Vue 3", "note": "eine eigene App pro Subdomain"},
                    {"name": "Pinia", "note": "Zustand je App, gemeinsame Anmeldung"},
                    {"name": "Vite", "note": "Entwicklung und Build"},
                    {
                        "name": "Tailwind CSS 4 und daisyUI",
                        "note": "Design aus einer gemeinsamen Basis",
                    },
                ],
            },
            {
                "title": "Backend",
                "items": [
                    {"name": "Django 6", "note": "ein Projekt, mehrere Apps"},
                    {
                        "name": "Django REST Framework",
                        "note": "ViewSets und Serializer je Aufgabe",
                    },
                    {"name": "PostgreSQL 17", "note": "Daten und Zwischenspeicher"},
                    {"name": "gunicorn", "note": "ein Worker mit acht Threads"},
                ],
            },
            {
                "title": "Suche",
                "items": [
                    {"name": "SearXNG", "note": "Metasuche mit eigenem Schutz-Plugin"},
                    {
                        "name": "Tor",
                        "note": "drei Instanzen, Kreise pro Anfrage getrennt",
                    },
                ],
            },
            {
                "title": "Betrieb",
                "items": [
                    {
                        "name": "Caddy",
                        "note": "Edge und Origin, automatische Zertifikate",
                    },
                    {"name": "Anubis", "note": "Bot-Schutz ohne Tracking"},
                    {"name": "Docker Compose", "note": "alle Dienste als Container"},
                    {
                        "name": "govex",
                        "note": "eigene Anmeldung für alle Apps über OIDC",
                    },
                ],
            },
        ],
    },
    {
        "kind": "principles",
        "title": "Prinzipien",
        "items": [
            {
                "title": "Logik im Backend",
                "text": "Rechte, Berechnungen und Markdown entstehen auf dem Server. Die Frontends zeigen nur an.",
            },
            {
                "title": "Eine gemeinsame Basis",
                "text": "Modelle, Serializer, Views, Berechtigungen und HTTP-Zugriffe kommen aus einer App. Neue Apps erben, statt zu kopieren.",
            },
            {
                "title": "Datensparsam",
                "text": "Keine Zugriffslogs, keine Tracker, keine Drittanbieter für Videos.",
            },
        ],
    },
    {
        "kind": "diagram",
        "title": "Code-Architektur",
        "text": (
            "Jedes Frontend ist eine eigene App. Das Backend ist ein einziges Django-Projekt "
            "mit mehreren Apps, die alle auf derselben Basis aufbauen."
        ),
        "columns": [
            {
                "title": "Frontends",
                "nodes": [
                    {"id": "fe-wintersehn", "label": "Wintersehn"},
                    {"id": "fe-home", "label": "Home"},
                    {"id": "fe-search", "label": "Suche"},
                    {"id": "fe-atlas", "label": "ATLAS"},
                    {"id": "fe-lumon", "label": "LUMON"},
                    {"id": "fe-monolith", "label": "MONOLITH"},
                ],
            },
            {
                "title": "Apps",
                "group": "Backend · Django",
                "nodes": [
                    {"id": "content", "label": "content", "note": "Inhalte, Rollen"},
                    {"id": "accounts", "label": "accounts", "note": "Anmeldung"},
                    {"id": "search", "label": "search"},
                    {"id": "atlas", "label": "atlas"},
                    {"id": "lumon", "label": "lumon"},
                    {"id": "monolith", "label": "monolith"},
                ],
            },
            {
                "title": "Gemeinsam",
                "group": "Backend · Django",
                "nodes": [
                    {
                        "id": "commons",
                        "label": "commons",
                        "note": "Modelle, Views, Rechte",
                    }
                ],
            },
        ],
        "edges": [
            ["fe-wintersehn", "content"],
            ["fe-home", "accounts"],
            ["fe-search", "search"],
            ["fe-atlas", "atlas"],
            ["fe-lumon", "lumon"],
            ["fe-monolith", "monolith"],
            ["content", "commons"],
            ["accounts", "commons"],
            ["search", "commons"],
            ["atlas", "commons"],
            ["lumon", "commons"],
            ["monolith", "commons"],
        ],
    },
    {
        "kind": "code",
        "title": "Ein Serializer pro Aufgabe",
        "text": (
            "Jede Ressource hat eine Gruppe von Serializern. Die gemeinsame Basis wählt "
            "automatisch den passenden: list für Übersichten, retrieve für Details, write für Eingaben."
        ),
        "file": "backend/commons/serializers.py",
        "code": SERIALIZER,
    },
    {
        "kind": "code",
        "title": "Sichtbarkeit an einer Stelle",
        "text": "Wer was sehen darf, entscheidet das QuerySet. Views rufen nur apply_acl auf.",
        "file": "backend/commons/models.py",
        "code": ACL,
    },
    {
        "kind": "flow",
        "title": "Ablauf der Anmeldung",
        "steps": [
            "«Anmelden» leitet zu govex weiter, mit einem einmaligen PKCE-Schlüssel.",
            "Nach der Anmeldung schickt govex einen einmaligen Code zurück.",
            "Das Backend tauscht den Code direkt beim Server gegen ein Token und liest die Nutzerdaten.",
            "Das Konto wird angelegt oder verknüpft. Die Sitzung gilt für alle Apps unter wintersehn.ch.",
            "Zustimmungen meldet Wintersehn signiert an govex. govex kann sie anzeigen, aber nicht fälschen.",
        ],
    },
    {
        "kind": "flow",
        "title": "Deploy ohne Ausfall",
        "steps": [
            "bin/release baut die Images für Backend, Proxy, SearXNG und Tor und lädt sie hoch.",
            "Auf dem Server startet bin/deploy ein zweites Backend mit dem neuen Image.",
            "Datenbank-Migrationen laufen beim Start automatisch.",
            "Erst wenn das neue Backend gesund meldet, übernimmt der Proxy und das alte stoppt.",
            "Proxy, Suche und Tor starten mit den neuen Images, alte Images werden gelöscht.",
        ],
    },
    {
        "kind": "group",
        "title": "Search",
        "text": "Private Suche über SearXNG und Tor.",
        "sites": [SITES["search"]],
    },
    {
        "kind": "diagram",
        "title": "Kommunikation der Suche",
        "text": (
            "Die Suchseite spricht über zwei Wege mit dem Server: Treffer kommen von SearXNG, "
            "Einstellungen und Sicherheitsbewertungen vom Django-Backend."
        ),
        "columns": [
            {
                "title": "Browser",
                "nodes": [{"id": "ui", "label": "Suche", "note": "Vue-App"}],
            },
            {
                "title": "Origin",
                "nodes": [
                    {
                        "id": "route-search",
                        "label": "/searxng/",
                        "note": "nur mit App-Header",
                    },
                    {
                        "id": "route-api",
                        "label": "/api/search/",
                        "note": "Einstellungen, Bewertung",
                    },
                ],
            },
            {
                "title": "Dienste",
                "nodes": [
                    {"id": "searxng", "label": "SearXNG", "note": "Schutz-Plugin"},
                    {"id": "django", "label": "Django", "note": "Doppelgänger-Prüfung"},
                ],
            },
            {
                "title": "Netz",
                "nodes": [
                    {"id": "tor", "label": "Tor", "note": "getrennte Kreise"},
                    {
                        "id": "observatory",
                        "label": "Mozilla Observatory",
                        "note": "Sicherheits-Header",
                    },
                ],
            },
            {
                "title": "Quellen",
                "nodes": [
                    {
                        "id": "engines",
                        "label": "Suchmaschinen",
                        "note": "DuckDuckGo, Startpage, …",
                    }
                ],
            },
        ],
        "edges": [
            ["ui", "route-search"],
            ["ui", "route-api"],
            ["route-search", "searxng"],
            ["route-api", "django"],
            ["searxng", "tor"],
            ["tor", "engines"],
            ["django", "observatory"],
        ],
    },
    {
        "kind": "flow",
        "title": "Ablauf einer Suche",
        "steps": [
            "Die Suchanfrage geht an das Backend der Suche.",
            "Ein Schutz-Plugin prüft die Anfrage auf verbotene Kombinationen.",
            "SearXNG fragt die Suchmaschinen über Tor ab, jede Anfrage über einen eigenen Kreis.",
            "Das Backend bewertet die Sicherheit der gefundenen Domains und erkennt Doppelgänger-Adressen.",
            "Bewertungen werden zwischengespeichert, damit dieselbe Domain nicht ständig neu geprüft wird.",
        ],
    },
    {
        "kind": "problem",
        "title": "Doppelgänger-Domains erkennen",
        "problem": (
            "Betrügerische Seiten tarnen sich mit Buchstaben aus anderen Schriften, etwa einem kyrillischen "
            "«а» statt einem lateinischen «a». Die Adresse sieht gleich aus, führt aber woandershin."
        ),
        "solution": (
            "Die Suche dekodiert jede Punycode-Adresse und bestimmt die Schrift jedes Buchstabens. "
            "Gemischte oder leicht verwechselbare Schriften lösen eine Warnung aus, bevor jemand klickt."
        ),
        "file": "backend/search/lookalike.py",
        "code": LOOKALIKE,
    },
    {
        "kind": "open",
        "title": "Noch offen",
        "items": [
            {
                "title": "Anonym suchen ohne Captchas",
                "text": (
                    "Manche Suchmaschinen sperren Tor-Ausgänge und Rechenzentren mit Drosselung oder Captchas. "
                    "Eine Suche, die anonym bleibt und trotzdem jede Quelle erreicht, ist noch nicht gelöst."
                ),
            },
            {
                "title": "Der Suchbegriff selbst",
                "text": (
                    "Anbieter sehen nicht, wer sucht, aber was gesucht wird. Wer persönliche Angaben "
                    "eintippt, verrät sie selbst. Dagegen hilft bisher nur Aufklärung."
                ),
            },
        ],
    },
    {
        "kind": "group",
        "title": "MONOLITH",
        "text": "Verschlüsselte Dossiers und ein Netz aus Beziehungen und Vertrauen.",
        "sites": [SITES["monolith"]],
    },
    {
        "kind": "problem",
        "title": "Verschlüsselt und trotzdem durchsuchbar",
        "problem": (
            "Sensible Texte liegen verschlüsselt in der Datenbank. Damit lassen sie sich nicht mehr "
            "suchen oder auf Eindeutigkeit prüfen, denn derselbe Text ergibt jedes Mal einen anderen Geheimtext."
        ),
        "solution": (
            "Neben dem verschlüsselten Wert speichert die Datenbank einen Blind Index: einen Hash mit "
            "geheimem Schlüssel. Gleiche Werte ergeben gleiche Hashes. Suche und Eindeutigkeit funktionieren, "
            "ohne dass der Klartext je in der Datenbank steht."
        ),
        "file": "backend/monolith/fields.py",
        "code": BLIND_INDEX,
    },
    {
        "kind": "formula",
        "title": "Blind Index",
        "graphic": "blind-index",
        "file": "backend/monolith/crypto.py",
        "code": DIGEST,
        "text": "Die Rechnung hinter der Suche in verschlüsselten Daten.",
        "formulas": [{"label": "Index", "expression": "h = HMAC-SHA256(k, x)"}],
        "note": (
            "Gleicher Klartext x ergibt immer denselben Index h. Ohne den geheimen Schlüssel k lässt sich "
            "x weder zurückrechnen noch durch Raten prüfen."
        ),
    },
    {
        "kind": "formula",
        "title": "Kräfte im Netzwerk-Graph",
        "graphic": "forces",
        "file": "frontend/monolith/src/components/NetworkGraph.vue",
        "code": REPULSION,
        "text": "MONOLITH ordnet Personen und Beziehungen mit einer eigenen physikalischen Simulation an.",
        "formulas": [
            {"label": "Abstossung", "expression": "Δv = s · α · d / max(‖d‖², 100)"},
            {"label": "Mindestlänge", "expression": "Δp = (Lₘᵢₙ − ‖d‖) / (2 ‖d‖) · d"},
        ],
        "note": (
            "d ist der Vektor zwischen zwei Knoten, s die eingestellte Stärke, α die Abkühlung der "
            "Simulation. Nicht verbundene Knoten stossen sich mit 1/‖d‖ ab, die Untergrenze 100 "
            "verhindert Sprünge, wenn zwei Knoten fast aufeinanderliegen. Zu kurze Linien werden "
            "symmetrisch auf ihre Mindestlänge gestreckt, damit die Beschriftung Platz hat."
        ),
    },
    {
        "kind": "formula",
        "title": "Linien entflechten",
        "graphic": "crossing",
        "file": "frontend/monolith/src/components/NetworkGraph.vue",
        "code": UNTANGLE,
        "text": "Damit das Netz lesbar bleibt, erkennt und löst der Graph Kreuzungen selbst.",
        "formulas": [
            {
                "label": "Orientierung",
                "expression": "o(p, q, r) = sgn((q − p) × (r − p))",
            },
            {
                "label": "Kreuzung",
                "expression": "AB ∩ CD ⇔ o(A, B, C) ≠ o(A, B, D) ∧ o(C, D, A) ≠ o(C, D, B)",
            },
            {
                "label": "Nächster Punkt",
                "expression": "t = clamp((P − A) · (B − A) / ‖B − A‖², 0, 1)",
            },
        ],
        "note": (
            "Kreuzen sich zwei Linien, schiebt die Simulation beide auseinander. Liegt ein Knoten näher "
            "als zwei Radien an einer fremden Linie, wird er vom nächsten Punkt A + t · (B − A) weggedrückt."
        ),
    },
    {
        "kind": "formula",
        "title": "Zoomen um den Cursor",
        "graphic": "zoom",
        "file": "frontend/monolith/src/mixins/panZoomMixin.js",
        "code": ZOOM,
        "text": "Beim Zoomen bleibt der Punkt unter dem Cursor oder zwischen zwei Fingern an seinem Platz.",
        "formulas": [
            {"label": "Massstab", "expression": "k′ = clamp(k · f, kₘᵢₙ, kₘₐₓ)"},
            {"label": "Verschiebung", "expression": "x′ = o − (o − x) · k′ / k"},
            {
                "label": "Faktor",
                "expression": "f = e^(−Δy / 500),  f = ‖c − p‖ / ‖c₀ − p‖",
            },
        ],
        "note": (
            "o ist der Punkt unter dem Cursor. Das Mausrad wirkt über die Exponentialfunktion gleichmässig, "
            "egal wie fein es auflöst. Beim Zoomen mit zwei Fingern zählt das Verhältnis der Fingerabstände."
        ),
    },
    {
        "kind": "formula",
        "title": "Vertrauenskreise",
        "graphic": "circles",
        "file": "frontend/monolith/src/components/TrustCircles.vue",
        "code": CIRCLES,
        "text": "Personen liegen auf Ringen um die Mitte, je näher, desto mehr Vertrauen.",
        "formulas": [
            {"label": "Winkel", "expression": "θᵢ = −π/2 + (i + ½) / n · 2π"},
            {"label": "Position", "expression": "(x, y) = (r · cos θᵢ, r · sin θᵢ)"},
            {"label": "Ring", "expression": "b = ⌈(√(x² + y²) − r₀) / w⌉"},
        ],
        "note": (
            "Die n Personen eines Rings verteilen sich gleichmässig, beginnend oben. Beim Ziehen bestimmt "
            "der Abstand zur Mitte, in welchen Ring jemand fällt."
        ),
    },
    {
        "kind": "group",
        "title": "LUMON",
        "text": "Filme und Serien aus der eigenen Mediathek.",
        "sites": [SITES["lumon"]],
    },
    {
        "kind": "problem",
        "title": "Grosse Uploads ohne Abbrüche",
        "problem": "Filme haben mehrere Gigabyte. Ein einzelner Upload sprengt Zeitlimits und blockiert den Server.",
        "solution": (
            "Der Browser schickt die Datei in Stücken zu 8 MB. Das Backend prüft bei jedem Stück die Position, "
            "damit nichts doppelt oder in falscher Reihenfolge landet, und hängt es direkt an die Datei an."
        ),
        "file": "backend/lumon/models.py",
        "code": UPLOAD,
    },
]

for section in ENGINEERING:
    if "file" in section:
        section["url"] = REPOSITORY + section["file"]


def seed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.get_or_create(key="engineering", defaults={"data": ENGINEERING})


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    SiteContent.objects.filter(key="engineering").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0024_seed_now"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
