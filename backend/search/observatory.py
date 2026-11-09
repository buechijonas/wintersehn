from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache

from commons.http import ServiceUnavailable, fetch

ANALYZE_URL = "https://observatory-api.mdn.mozilla.net/api/v2/analyze"
DETAILS_URL = "https://developer.mozilla.org/en-US/observatory/analyze"
RATINGS = {
    "A+": "secure",
    "A": "secure",
    "A-": "secure",
    "B+": "neutral",
    "B": "neutral",
    "B-": "neutral",
    "C+": "neutral",
    "C": "neutral",
    "C-": "neutral",
    "D+": "insecure",
    "D": "insecure",
    "D-": "insecure",
    "F": "insecure",
}
REPORT_TIMEOUT = 60 * 60 * 24 * 7
UNKNOWN_TIMEOUT = 60 * 60 * 24
UNKNOWN = {}


def cache_key(host):
    return f"observatory-report:{host}"


def report(host, data):
    return {
        "grade": data["scan"]["grade"],
        "score": data["scan"]["score"],
        "url": f"{DETAILS_URL}?host={host}",
        "tests": [
            {"name": name, "passed": test["pass"]}
            for name, test in data["tests"].items()
            if test["pass"] is not None
        ],
    }


def fetch_report(host):
    try:
        response = fetch("post", ANALYZE_URL, timeout=8, params={"host": host})
    except ServiceUnavailable:
        return UNKNOWN
    data = response.json()
    if not data.get("scan", {}).get("grade"):
        return UNKNOWN
    return report(host, data)


def store_report(host, host_report):
    timeout = REPORT_TIMEOUT if host_report else UNKNOWN_TIMEOUT
    cache.set(cache_key(host), host_report, timeout)


def reports(hosts):
    cached = cache.get_many([cache_key(host) for host in hosts])
    known = {
        host: cached[cache_key(host)] for host in hosts if cache_key(host) in cached
    }
    missing = [host for host in hosts if host not in known]
    with ThreadPoolExecutor(max_workers=8) as pool:
        fetched = dict(zip(missing, pool.map(fetch_report, missing)))
    for host, host_report in fetched.items():
        store_report(host, host_report)
    return {**known, **fetched}


def ratings(hosts):
    return {
        host: {**host_report, "rating": RATINGS[host_report["grade"]]}
        for host, host_report in reports(hosts).items()
        if host_report.get("grade") in RATINGS
    }
