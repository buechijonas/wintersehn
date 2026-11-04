import os
from pathlib import Path

import yaml

UPSTREAM_SETTINGS = Path("/usr/local/searxng/searx/settings.yml")
PROXIES = {
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
    proxies = {name: {"all://": [proxy]} for name, proxy in PROXIES.items() if proxy}
    networks = {"direct": {}, **proxies}

    settings["outgoing"]["networks"] = {
        name: {"using_tor_proxy": False, "proxies": network_proxies}
        for name, network_proxies in networks.items()
    }
    variants = [variant(engine, name) for name in networks for engine in engines]
    settings["engines"] = settings.get("engines", []) + variants
    keep_only.extend(engine["name"] for engine in variants)

    Path(os.environ["SEARXNG_SETTINGS_PATH"]).write_text(yaml.safe_dump(settings))


main()
