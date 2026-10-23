from .models import (
    Event,
    Relationship,
    Stance,
    TrustEntry,
    Visibility,
)
from .serializers import DossierDetailSerializer

FULL = Visibility.FULL
SHOWN = {
    Visibility.VISIBLE: {"label", "value", "links"},
    Visibility.VALUE: {"label"},
    Visibility.FULL: set(),
}


def item(target, label, value=None, links=()):
    return {"target": target, "label": label, "value": value, "links": list(links)}


def title_item(share):
    return item("title", "title", share.dossier.title)


def meta_items(share):
    fields = DossierDetailSerializer(share.dossier).data
    return [
        item(f"field:{field}", field, fields[field])
        for field in fields
        if field not in ("uuid", "title")
    ]


def event_links(event):
    return [
        *dict.fromkeys(f"stance:{stance.topic}" for stance in event.stances.all()),
        *(f"addiction:{addiction.pk}" for addiction in event.addictions.all()),
        *(f"reference:{reference.uuid}" for reference in event.references.all()),
        *(
            f"relationship:{relationship.other(event.dossier).uuid}"
            for relationship in event.relationships.all()
        ),
    ]


def event_items(share):
    events = Event.objects.with_links().filter(dossier=share.dossier)
    return [
        item(
            f"event:{event.uuid}",
            {"date": event.date.isoformat(), "title": event.title},
            event.text,
            event_links(event),
        )
        for event in events
    ]


def relationship_items(share):
    dossier = share.dossier
    return [
        item(
            f"relationship:{relationship.other(dossier).uuid}",
            relationship.other(dossier).title,
            relationship.status_for(dossier),
        )
        for relationship in Relationship.objects.of(dossier)
    ]


def trust_items(share):
    ledger = TrustEntry.objects.ledger(share.created_by, share.dossier)
    summary = {key: ledger[key] for key in ("points", "level", "suggested_level")}
    return [
        item("trust:summary", {"kind": "summary"}, summary),
        *(
            item(
                f"trust_entry:{entry.uuid}",
                {"kind": "entry", "conduct": entry.conduct, "points": entry.points},
                {"date": entry.date.isoformat(), "text": entry.text},
            )
            for entry in ledger["entries"]
        ),
    ]


def stance_items(share):
    return [
        item(f"stance:{stance.topic}", stance.topic, stance.tags)
        for stance in Stance.objects.by_topic(share.dossier)
        if stance.tags
    ]


def addiction_items(share):
    return [
        item(f"addiction:{addiction.pk}", addiction.kind, addiction.frequency)
        for addiction in share.dossier.addictions.all()
    ]


def reference_items(share):
    return [
        item(
            f"reference:{reference.uuid}",
            {"icon": reference.icon, "name": reference.name},
            reference.url,
        )
        for reference in share.dossier.references.all()
    ]


SECTIONS = {
    "meta": meta_items,
    "events": event_items,
    "relationships": relationship_items,
    "trust": trust_items,
    "ideology": stance_items,
    "addictions": addiction_items,
    "references": reference_items,
}


BREADCRUMBS = ("root", "tab")


def document(share):
    return {
        "breadcrumbs": [item(f"breadcrumb:{level}", level) for level in BREADCRUMBS],
        "title": title_item(share),
        "sections": [
            {"key": key, "target": f"section:{key}", "items": build(share)}
            for key, build in SECTIONS.items()
        ],
    }


def targets(share):
    doc = document(share)
    return {
        doc["title"]["target"],
        *(crumb["target"] for crumb in doc["breadcrumbs"]),
        *(section["target"] for section in doc["sections"]),
        *(entry["target"] for section in doc["sections"] for entry in section["items"]),
    }


def with_visibility(entry, rules):
    return {**entry, "visibility": rules.get(entry["target"], FULL)}


def editable(share):
    rules = share.rule_map()
    doc = document(share)
    return {
        "breadcrumbs": [with_visibility(crumb, rules) for crumb in doc["breadcrumbs"]],
        "title": with_visibility(doc["title"], rules),
        "sections": [
            {
                **with_visibility(section, rules),
                "items": [with_visibility(entry, rules) for entry in section["items"]],
            }
            for section in doc["sections"]
        ],
    }


class Redactor:
    def __init__(self, share):
        self.rules = share.rule_map()
        self.doc = document(share)
        self.sections = {
            entry["target"]: section
            for section in self.doc["sections"]
            for entry in section["items"]
        }
        self.items = {
            entry["target"]: entry
            for section in self.doc["sections"]
            for entry in section["items"]
        }

    def visibility(self, target):
        return self.rules.get(target, FULL)

    def effective(self, target):
        section = self.sections[target]
        if self.visibility(section["target"]) != Visibility.VISIBLE:
            return FULL
        return self.visibility(target)

    def link(self, target):
        visibility = self.effective(target)
        shown = visibility != FULL
        return {
            "visibility": visibility,
            "section": self.sections[target]["key"] if shown else None,
            "label": self.items[target]["label"] if shown else None,
        }

    def redact(self, entry, visibility):
        shown = SHOWN[visibility]
        return {
            "visibility": visibility,
            "label": entry["label"] if "label" in shown else None,
            "value": entry["value"] if "value" in shown else None,
            "links": (
                [self.link(target) for target in entry["links"]]
                if "links" in shown
                else []
            ),
        }

    def section(self, section):
        visibility = self.visibility(section["target"])
        return {
            "visibility": visibility,
            "key": section["key"] if visibility != FULL else None,
            "items": [
                self.redact(entry, self.effective(entry["target"]))
                for entry in section["items"]
            ],
        }

    def result(self):
        return {
            "breadcrumbs": {
                crumb["label"]: self.visibility(crumb["target"]) == Visibility.VISIBLE
                for crumb in self.doc["breadcrumbs"]
            },
            "title": self.redact(self.doc["title"], self.visibility("title")),
            "sections": [self.section(section) for section in self.doc["sections"]],
        }


def redacted(share):
    return Redactor(share).result()


def shared_title(share):
    visible = share.visibility("title") == Visibility.VISIBLE
    return share.dossier.title if visible else None
