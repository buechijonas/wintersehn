from .countries import EU_MEMBERS

MAX_FOOTPRINT = 10
MIN_WEIGHT = 0.25
EU_FLAG = "european_union"


def privacy_section(sections):
    items = (item for section in sections for item in section["items"])
    return next((item for item in items if item.get("privacy")), None)


def flag(country):
    return EU_FLAG if country in EU_MEMBERS else country


def unique_services(services):
    return list({service["name"]: service for service in services}.values())


def totals_by(services, key):
    totals = {}
    for service in services:
        icon = key(service.get("country"))
        total = totals.setdefault(icon, {"icon": icon, "value": 0, "services": []})
        total["value"] += service["footprint"]
        total["services"].append(service["name"])
    return sorted(totals.values(), key=lambda total: total["value"], reverse=True)


def country_totals(services):
    return totals_by(services, lambda country: country)


def share(total, value):
    return {
        "icon": total["icon"],
        "label": ", ".join(total["services"]),
        "value": total["value"],
        "share": round(total["value"] / value * 100),
    }


def summarize(services, peak, scale):
    value = sum(service["footprint"] for service in services)
    return {
        "value": value,
        "max": scale,
        "countries": [
            {
                **share(country, value),
                "weight": MIN_WEIGHT + (1 - MIN_WEIGHT) * country["value"] / peak,
            }
            for country in country_totals(services)
        ],
        "regions": [share(region, value) for region in totals_by(services, flag)],
    }


def section_flags(items):
    services = items + [
        replaced for item in items for replaced in item.get("replaces", [])
    ]
    return {
        service["country"]: flag(service["country"])
        for service in services
        if service.get("country")
    }


def footprint(section):
    all_items = [item for group in section["groups"] for item in group["items"]]
    items = [item for item in all_items if not item.get("planned")]
    before = unique_services(
        [replaced for item in items for replaced in item.get("replaces", [])]
        + [item for item in items if item.get("dropped")]
    )
    after = unique_services([item for item in items if not item.get("dropped")])
    peak = max(country["value"] for country in country_totals(before))
    scale = max(len(before), len(after)) * MAX_FOOTPRINT
    before_summary = summarize(before, peak, scale)
    after_summary = summarize(after, peak, scale)
    return {
        "before": before_summary,
        "after": after_summary,
        "reduction": round(
            (1 - after_summary["value"] / before_summary["value"]) * 100
        ),
        "flags": section_flags(all_items),
    }
