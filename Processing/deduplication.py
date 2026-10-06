import hashlib
import re


def make_fingerprint(rec):
    if rec["source"] == "Books to Scrape":
        key = f'{rec["source"]} {rec["name_or_title"]}'
    else:
        key = f'{rec["source"]} {rec["author"]} {rec["name_or_title"][:50]}'

    key = re.sub(r"[^\w\s]", "", key.lower())
    key = " ".join(key.split())

    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def find_duplicates(records):
    seen = set()
    unique = []
    duplicates = []

    for rec in records:
        fingerprint = make_fingerprint(rec)

        if fingerprint in seen:
            duplicates.append(rec)
        else:
            unique.append(rec)
            seen.add(fingerprint)

    return unique, duplicates
    