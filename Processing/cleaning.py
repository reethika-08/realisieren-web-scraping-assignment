import re


RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}


def clean_text(raw):
    """
    Remove extra whitespace from text.
    """
    if raw is None:
        return ""

    return " ".join(str(raw).split())


def clean_price(raw):
    """
    Extract a numeric price from a raw price string.
    Example: '£51.77' -> 51.77
    """
    if not raw:
        return None

    cleaned = str(raw).replace(",", "")

    match = re.search(r"\d+(?:\.\d+)?", cleaned)

    if match:
        return float(match.group())

    return None


def clean_rating(raw):
    """
    Convert rating words into numbers.
    Example: 'star-rating Three' -> 3
    """
    text = str(raw or "").lower()

    for word in text.split():
        if word in RATING_MAP:
            return RATING_MAP[word]

    return None