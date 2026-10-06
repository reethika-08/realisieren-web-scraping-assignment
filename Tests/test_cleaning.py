from Processing.cleaning import clean_text, clean_price, clean_rating


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("star-rating Three") == 3