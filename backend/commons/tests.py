import ast
import io
import re
import tokenize
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.test import SimpleTestCase
from rest_framework.views import APIView

from commons.http import USER_AGENT
from commons.views import BaseViewSet
from main.urls import urlpatterns

BASE_DIR = Path(settings.BASE_DIR)
SKIPPED = {".venv", "migrations", "__pycache__", "site-packages"}
FORBIDDEN_NAMES = {"getattr", "setattr", "hasattr", "isinstance"}
HTTP_LIBRARIES = {"requests", "urllib3", "httpx", "urllib.request"}
HTTP_MODULE = "commons/http.py"
EXPLAINED = {"wintersehn/accounts/oidc.py", "wintersehn/accounts/models.py"}
MAX_NESTING = 2
MAX_LITERAL_SIZE = 100
MAX_MODELS_LINES = 500
CHOICE_VALUE = re.compile(r"[A-Za-z0-9_+-]+")


class Names(ast.NodeVisitor):
    def __init__(self):
        self.found = []

    def visit_Name(self, node):
        if node.id in FORBIDDEN_NAMES:
            self.found.append(node.id)


class Imports(ast.NodeVisitor):
    def __init__(self):
        self.found = []

    def visit_Import(self, node):
        self.found += [alias.name for alias in node.names]

    def visit_ImportFrom(self, node):
        self.found.append(node.module or "")


class Nesting(ast.NodeVisitor):
    def __init__(self):
        self.depth = 0
        self.found = []

    def block(self, node):
        self.depth += 1
        if self.depth > MAX_NESTING:
            self.found.append(node.lineno)
        self.generic_visit(node)
        self.depth -= 1

    visit_For = visit_While = visit_If = visit_With = visit_Try = block


class Literals(ast.NodeVisitor):
    def __init__(self):
        self.found = []

    def visit_Module(self, node):
        for statement in node.body:
            self.visit(statement)

    def visit_Assign(self, node):
        if size(node.value) > MAX_LITERAL_SIZE:
            self.found.append(ast.unparse(node.targets[0]))

    def generic_visit(self, node):
        pass


class Constants(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_Constant(self, node):
        self.count += 1


def size(value):
    try:
        ast.literal_eval(value)
    except ValueError:
        return 0
    constants = Constants()
    constants.visit(value)
    return constants.count


def sources():
    return [
        path
        for path in BASE_DIR.rglob("*.py")
        if not SKIPPED & set(path.relative_to(BASE_DIR).parts)
    ]


def relative(path):
    return str(path.relative_to(BASE_DIR))


def found(visitor_class, path):
    visitor = visitor_class()
    visitor.visit(ast.parse(path.read_text()))
    return visitor.found


def findings(visitor_class):
    results = {relative(path): found(visitor_class, path) for path in sources()}
    return {path: names for path, names in results.items() if names}


def comments(path):
    tokens = tokenize.generate_tokens(io.StringIO(path.read_text()).readline)
    return [
        token.start[0]
        for token in tokens
        if token.type == tokenize.COMMENT and not token.string.startswith("#!")
    ]


def project_apps():
    return [
        config
        for config in apps.get_app_configs()
        if Path(config.path).is_relative_to(BASE_DIR)
        and not SKIPPED & set(Path(config.path).relative_to(BASE_DIR).parts)
    ]


def subclasses(cls):
    return [
        subclass
        for child in cls.__subclasses__()
        for subclass in [child, *subclasses(child)]
    ]


class StyleTest(SimpleTestCase):
    def test_no_reflection(self):
        self.assertEqual(findings(Names), {})

    def test_no_comments(self):
        commented = {
            relative(path): comments(path)
            for path in sources()
            if relative(path) not in EXPLAINED
        }
        self.assertEqual(
            {path: lines for path, lines in commented.items() if lines}, {}
        )

    def test_flat_blocks(self):
        self.assertEqual(findings(Nesting), {})

    def test_data_lives_in_files(self):
        self.assertEqual(findings(Literals), {})

    def test_requests_go_through_commons(self):
        imports = findings(Imports)
        direct = {
            path: sorted(HTTP_LIBRARIES & set(modules))
            for path, modules in imports.items()
            if path != HTTP_MODULE
        }
        self.assertEqual({path: names for path, names in direct.items() if names}, {})

    def test_requests_identify_as_wintersehn(self):
        self.assertTrue(USER_AGENT.startswith("wintersehn "))

    def test_large_models_are_packages(self):
        long = {
            relative(path): len(path.read_text().splitlines())
            for path in sources()
            if path.name == "models.py"
        }
        self.assertEqual(
            {path: lines for path, lines in long.items() if lines > MAX_MODELS_LINES},
            {},
        )

    def test_choice_values_are_english(self):
        values = [
            (model.__name__, field.name, value)
            for config in project_apps()
            for model in config.get_models()
            for field in model._meta.fields
            for value, _ in field.choices or []
        ]
        self.assertTrue(values)
        self.assertEqual(
            [entry for entry in values if not CHOICE_VALUE.fullmatch(str(entry[2]))],
            [],
        )

    def test_views_build_on_commons(self):
        self.assertTrue(urlpatterns)
        names = tuple(f"{config.name}." for config in project_apps())
        views = [
            view for view in subclasses(APIView) if view.__module__.startswith(names)
        ]
        self.assertTrue(views)
        self.assertEqual(
            [view for view in views if not issubclass(view, BaseViewSet)], []
        )

    def test_storage_is_namespaced(self):
        self.assertTrue(settings.SESSION_COOKIE_NAME.startswith("wntrs_"))
        self.assertTrue(settings.CSRF_COOKIE_NAME.startswith("wntrs_"))
        self.assertEqual(settings.CACHES["default"]["KEY_PREFIX"], "wntrs")
