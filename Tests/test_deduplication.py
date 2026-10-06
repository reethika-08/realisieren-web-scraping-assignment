from Processing.deduplication import find_duplicates


def test_duplicate_books():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Test Book",
            "author": ""
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "  test   book  ",
            "author": ""
        }
    ]

    unique, duplicates = find_duplicates(records)

    assert len(unique) == 1
    assert len(duplicates) == 1


def test_unique_records():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Book One",
            "author": ""
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Book Two",
            "author": ""
        }
    ]

    unique, duplicates = find_duplicates(records)

    assert len(unique) == 2
    assert len(duplicates) == 0