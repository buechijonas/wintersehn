import os
from pathlib import Path

import yaml

UPSTREAM_SETTINGS = Path("/usr/local/searxng/searx/settings.yml")
NETWORKS = {
    "vpn": os.environ.get("SEARXNG_VPN_PROXY", ""),
    "proxy": os.environ.get("SEARXNG_CUSTOM_PROXY", ""),
}


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
    engines = [engine for engine in upstream if engine["name"] in keep_only]
    networks = {name: proxy for name, proxy in NETWORKS.items() if proxy}

    settings["outgoing"]["networks"] = {
        name: {"using_tor_proxy": False, "proxies": {"all://": [proxy]}}
        for name, proxy in networks.items()
    }
    variants = [variant(engine, name) for name in networks for engine in engines]
    settings["engines"] = settings.get("engines", []) + variants
    keep_only.extend(engine["name"] for engine in variants)

    Path(os.environ["SEARXNG_SETTINGS_PATH"]).write_text(yaml.safe_dump(settings))


main()
