import json
from pathlib import Path

COUNTRIES = json.loads((Path(__file__).parent / "countries.json").read_bytes())
COUNTRY_CODES = COUNTRIES["codes"]
COUNTRY_POINTS = COUNTRIES["points"]
EU_MEMBERS = set(COUNTRIES["eu_members"])
