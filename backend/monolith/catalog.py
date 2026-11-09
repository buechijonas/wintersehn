import json
from pathlib import Path

TAGS = json.loads((Path(__file__).parent / "catalog.json").read_bytes())
CATALOG = TAGS["catalog"]
CHARACTER = TAGS["character"]
CONDUCT_TRAITS = TAGS["conduct_traits"]

WEIGHTS = {
    topic: {tag: weight for tags in groups.values() for tag, weight in tags.items()}
    for topic, groups in CATALOG.items()
}

SPECTRUM = {
    "politics": 1,
    "economy": 1,
    "society": 1,
    "migration": 1,
    "religion": 1,
    "foreign_policy": -1,
    "environment": -1,
}

COMPASS = {
    "economy": ["economy", "politics"],
    "freedom": ["ideology", "domestic_policy"],
    "society": ["society", "migration", "religion"],
}

CONDUCT_POINTS = {
    "promise_kept": 2,
    "promise_broken": -3,
    "punctual": 1,
    "late": -1,
    "cancelled": -2,
    "secret_kept": 2,
    "secret_shared": -3,
    "supported": 2,
    "let_down": -2,
    "honest": 1,
    "lied": -3,
    "debt_repaid": 1,
    "debt_unpaid": -2,
    "fault_admitted": 2,
    "fault_denied": -2,
    "competed": -1,
}
