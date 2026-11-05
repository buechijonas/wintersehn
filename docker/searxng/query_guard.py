import re
import typing as t
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml
from searx.plugins import Plugin, PluginInfo
from searx.plugins._core import PluginStorage
from searx.result_types import Answer

DIRECTORY = Path("/usr/local/searxng/config/query_guard")
EXACT_LENGTH = 5
INNER_LENGTH = 6
MINOR_AGES = range(1, 18)
SYMBOLS = str.maketrans({"@": "a", "$": "s", "€": "e"})
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t"})
CJK = re.compile(r"[぀-ヿ㐀-鿿豈-﫿]")
SPACED_LETTERS = re.compile(r"(?<!\w)(?:\w )+\w(?!\w)")
STRICT_CATEGORIES = {"sensitive_zh"}
RULES = [
    ("child_abuse", [{"minor"}, {"sexual"}]),
    ("non_consensual", [{"covert", "deepfake"}, {"intimate"}]),
    ("mass_harm", [{"agent"}, {"produce", "purchase"}]),
    ("weapons", [{"explosive"}, {"produce", "purchase"}]),
    ("weapons", [{"weapon", "weapon_part"}, {"illegal_source", "conversion"}]),
    ("weapons", [{"untraceable"}, {"weapon", "weapon_part"}]),
    ("weapons", [{"weapon_part"}, {"produce"}]),
    ("drugs", [{"drug"}, {"purchase", "produce"}]),
    ("sensitive_zh", [{"zh_leader"}, {"zh_criticism"}]),
]


def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower().translate(SYMBOLS))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = re.sub(r"[^\w]+", " ", text)
    text = SPACED_LETTERS.sub(lambda match: match.group(0).replace(" ", ""), text)
    return " ".join(text.split())


def deleet(token):
    return token.translate(LEET) if re.search(r"[^\W\d_]", token) else token


class Query:
    def __init__(self, raw):
        self.text = normalize(raw)
        self.tokens = [deleet(token) for token in self.text.split()]
        self.spaced = f" {' '.join(self.tokens)} "
        self.compact = "".join(self.tokens)


class Term:
    def __init__(self, raw):
        self.text = " ".join(deleet(token) for token in normalize(raw).split())
        self.compact = self.text.replace(" ", "")

    def matches(self, query):
        if CJK.search(self.text):
            return self.compact in query.compact
        if " " in self.text:
            return f" {self.text} " in query.spaced or self.inside(query)
        if len(self.text) < EXACT_LENGTH:
            return self.text in query.tokens
        return any(token.startswith(self.text) for token in query.tokens) or self.inside(query)

    def inside(self, query):
        return len(self.compact) >= INNER_LENGTH and self.compact in query.compact


class GuardAnswer(Answer, kw_only=True):
    category: str
    link_title: str = ""
    content: str = ""


class Guard:
    def __init__(self, directory):
        self.groups = defaultdict(list)
        self.terms = defaultdict(list)
        self.messages = yaml.safe_load((directory / "messages.yml").read_text(encoding="utf-8"))
        suffixes = set()
        for path in sorted((directory / "lists").glob("*.yml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            for name, words in data["groups"].items():
                self.groups[name] += [Term(word) for word in words]
            for category, words in data["terms"].items():
                self.terms[category] += [Term(word) for word in words]
            suffixes |= {re.escape(normalize(suffix)) for suffix in data["age_suffixes"]}
        ages = "|".join(str(age) for age in reversed(MINOR_AGES))
        endings = "|".join(sorted(suffixes, key=len, reverse=True))
        self.minor_age = re.compile(rf"(?<!\d)(?:{ages})\s*(?:{endings})(?!\w)")

    def found(self, query):
        groups = {
            name for name, terms in self.groups.items() if any(term.matches(query) for term in terms)
        }
        if self.minor_age.search(query.text):
            groups.add("minor")
        return groups

    def matching(self, query, groups):
        for category, terms in self.terms.items():
            if any(term.matches(query) for term in terms):
                yield category
        for category, required in RULES:
            if all(groups & options for options in required):
                yield category

    def category(self, raw):
        query = Query(raw)
        groups = self.found(query)
        categories = list(self.matching(query, groups))
        strict = [category for category in categories if category in STRICT_CATEGORIES]
        if strict:
            return strict[0]
        if "context" in groups and "seeking" not in groups:
            return None
        return next(iter(categories), None)

    def answer(self, raw):
        category = self.category(raw)
        if not category:
            return None
        return GuardAnswer(category=category, **self.messages[category])


GUARD = Guard(DIRECTORY)
run_pre_search = PluginStorage.pre_search


def guarded_pre_search(self, request, search):
    answer = GUARD.answer(search.search_query.query)
    if not answer:
        return run_pre_search(self, request, search)
    search.result_container.answers.add(answer)
    return False


PluginStorage.pre_search = guarded_pre_search


@t.final
class SXNGPlugin(Plugin):
    id = "query_guard"

    def __init__(self, plg_cfg):
        super().__init__(plg_cfg)
        self.info = PluginInfo(
            id=self.id,
            name="Query guard",
            description="Stops searches for abuse material, weapons and drug sales",
            preference_section=None,
        )
