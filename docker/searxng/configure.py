import os
import secrets
from pathlib import Path

import yaml

UPSTREAM_SETTINGS = Path("/usr/local/searxng/searx/settings.yml")
STRICT_CIRCUITS = 4
BRAVE_API_KEY = os.environ.get("SEARXNG_BRAVE_API_KEY", "")
BRAVE_API = {
    "name": "braveapi",
    "shortcut": "bra",
    "api_key": BRAVE_API_KEY,
    "inactive": False,
}


def strict_proxies(tor_proxies):
    return [
        proxy.replace("://", f"://{secrets.token_hex(8)}:x@", 1)
        for _ in range(STRICT_CIRCUITS)
        for proxy in tor_proxies
    ]


def strict_variant(engine):
    return {
        **engine,
        "name": f"{engine['name']} strict",
        "shortcut": f"{engine['shortcut']}-strict",
        "network": "strict",
        "disabled": False,
        "inactive": False,
    }


def main():
    settings = yaml.safe_load(Path(os.environ["SEARXNG_BASE_SETTINGS"]).read_text())
    upstream = yaml.safe_load(UPSTREAM_SETTINGS.read_text())["engines"]
    keep_only = settings["use_default_settings"]["engines"]["keep_only"]
    if BRAVE_API_KEY:
        keep_only.append(BRAVE_API["name"])
        settings["engines"] = settings.get("engines", []) + [BRAVE_API]
    engines = [
        {**engine, **BRAVE_API} if engine["name"] == BRAVE_API["name"] else engine
        for engine in upstream
        if engine["name"] in keep_only
    ]
    tor_proxies = settings["outgoing"].get("proxies", {}).get("all://", [])
    variants = [strict_variant(engine) for engine in engines if tor_proxies]

    settings["outgoing"]["networks"] = {
        "strict": {"using_tor_proxy": False, "proxies": {"all://": strict_proxies(tor_proxies)}}
    }
    settings["engines"] = settings.get("engines", []) + variants
    keep_only.extend(engine["name"] for engine in variants)

    Path(os.environ["SEARXNG_SETTINGS_PATH"]).write_text(yaml.safe_dump(settings))


main()
