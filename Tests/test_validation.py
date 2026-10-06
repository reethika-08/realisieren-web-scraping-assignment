from Processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": 10.99,
        "rating": 4
    }

    assert validate_record(record) == []


def test_missing_name():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "",
        "price": 10.99,
        "rating": 4
    }

    assert "missing_name" in validate_record(record)


def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": 10.99,
        "rating": 6
    }

    assert "invalid_rating" in validate_record(record)