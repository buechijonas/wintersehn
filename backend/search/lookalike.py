import unicodedata

PUNYCODE_PREFIX = "xn--"
CONFUSABLE_SCRIPTS = {"CYRILLIC", "GREEK", "ARMENIAN", "CHEROKEE"}


def decode_label(label):
    if not label.startswith(PUNYCODE_PREFIX):
        return label
    try:
        return label[len(PUNYCODE_PREFIX) :].encode("ascii").decode("punycode")
    except UnicodeError:
        return None


def scripts(label):
    return {
        unicodedata.name(char, "UNKNOWN").split(" ")[0]
        for char in label
        if char.isalpha()
    }


def is_lookalike(label):
    if label is None:
        return True
    found = scripts(label)
    return len(found) > 1 or bool(found & CONFUSABLE_SCRIPTS)


def check(host):
    labels = [decode_label(label) for label in host.split(".")]
    punycode = [
        label
        for label, original in zip(labels, host.split("."))
        if original.startswith(PUNYCODE_PREFIX)
    ]
    if not any(is_lookalike(label) for label in punycode):
        return None
    return {"lookalike": True, "unicode": ".".join(label or "?" for label in labels)}


def lookalikes(hosts):
    return {host: report for host in hosts if (report := check(host))}
