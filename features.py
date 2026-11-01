
import re
import ipaddress
from urllib.parse import urlparse

FEATURE_NAMES = [
    "url_length", "hostname_length", "path_length", "num_dots",
    "num_hyphens", "num_at", "num_question", "num_equal",
    "num_ampersand", "num_slash", "num_digits", "num_subdomains",
    "has_ip", "has_https", "has_shortener", "suspicious_word_count"
]

SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "update", "account", "confirm",
    "bank", "wallet", "signin", "password", "free", "reward"
]

SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly"]

def extract_features(url):
    original = str(url).strip()
    work_url = original if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", original) else "http://" + original
    parsed = urlparse(work_url)
    hostname = parsed.netloc.split("@")[-1].split(":")[0].lower()
    path = parsed.path or ""

    try:
        ipaddress.ip_address(hostname)
        has_ip = 1
    except Exception:
        has_ip = 0

    labels = [x for x in hostname.split(".") if x]
    num_subdomains = max(0, len(labels) - 2)

    lower = original.lower()
    suspicious_count = sum(lower.count(w) for w in SUSPICIOUS_WORDS)
    has_shortener = int(any(s in lower for s in SHORTENERS))

    return [
        len(original), len(hostname), len(path), original.count("."),
        original.count("-"), original.count("@"), original.count("?"),
        original.count("="), original.count("&"), original.count("/"),
        sum(c.isdigit() for c in original), num_subdomains,
        has_ip, int(work_url.lower().startswith("https://")),
        has_shortener, suspicious_count
    ]
