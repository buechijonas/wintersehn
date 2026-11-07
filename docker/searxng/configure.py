import os
import secrets
from pathlib import Path

import yaml

UPSTREAM_SETTINGS = Path("/usr/local/searxng/searx/settings.yml")
STRICT_CIRCUITS = 4
TOR_BLOCKED = {"mojeek", "mojeek images", "mojeek news"}
PROXIES = {
    "vpn": os.environ.get("SEARXNG_VPN_PROXY", ""),
    "proxy": os.environ.get("SEARXNG_CUSTOM_PROXY", ""),
}
BRAVE_API_KEY = os.environ.get("SEARXNG_BRAVE_API_KEY", "")
BRAVE_API = {
    "name": "braveapi",
    "shortcut": "bra",
    "api_key": BRAVE_API_KEY,
    "inactive": False,
}


def proxy_list(value):
    return [proxy.strip() for proxy in value.split(",") if proxy.strip()]


def strict_proxies(tor_proxies):
    return [
        proxy.replace("://", f"://{secrets.token_hex(8)}:x@", 1)
        for _ in range(STRICT_CIRCUITS)
        for proxy in tor_proxies
    ]


def variant(engine, network):
    return {
        **engine,
        "name": f"{engine['name']} {network}",
        "shortcut": f"{engine['shortcut']}-{network}",
        "network": network,
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
    proxies = {
        name: {"all://": proxy_list(value)}
        for name, value in PROXIES.items()
        if proxy_list(value)
    }
    tor_proxies = settings["outgoing"].get("proxies", {}).get("all://", [])
    strict = {"strict": {"all://": strict_proxies(tor_proxies)}} if tor_proxies else {}
    networks = {"direct": {}, **strict, **proxies}

    settings["outgoing"]["networks"] = {
        name: {"using_tor_proxy": False, "proxies": network_proxies}
        for name, network_proxies in networks.items()
    }
    tor_networks = {"strict"}
    variants = [
        variant(engine, name)
        for name in networks
        for engine in engines
        if not (name in tor_networks and engine["name"] in TOR_BLOCKED)
    ]
    settings["engines"] = [
        engine
        for engine in settings.get("engines", []) + variants
        if engine["name"] not in TOR_BLOCKED
    ]
    keep_only[:] = [name for name in keep_only if name not in TOR_BLOCKED]
    keep_only.extend(engine["name"] for engine in variants)

    Path(os.environ["SEARXNG_SETTINGS_PATH"]).write_text(yaml.safe_dump(settings))


main()
