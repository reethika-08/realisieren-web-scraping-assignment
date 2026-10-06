# Realisieren Technologies - Web Scraping Assignment

## 1. Project Overview

This project is a Python-based web scraping and data processing pipeline developed for the Realisieren Technologies Python Web Scraping Interview Assignment.

The application collects public data from:

* Books to Scrape
* Quotes to Scrape

The collected data is processed through the following ETL pipeline:

```text
Scrape → Clean → Validate → Deduplicate → Consolidate → Save
```

The final solution produces:

* A consolidated CSV dataset
* A JSON summary report
* An execution log

The implementation uses Python, Requests, BeautifulSoup, and pytest.

---

## 2. Websites Scraped

### Books to Scrape

URL:

https://books.toscrape.com/

The scraper collects book information including:

* Book title
* Price
* Rating
* Category
* Product URL
* Source name

The scraper follows the `Next` pagination link until all available pages are processed.

### Quotes to Scrape

URL:

https://quotes.toscrape.com/

The scraper collects:

* Quote text
* Author
* Tags
* Page URL
* Source name

The scraper follows the `Next` pagination link until all available pages are processed.

No authentication, CAPTCHA bypass, or restricted information is used.

---

## 3. Project Structure

```text
Scrapping_assignment/
│
├── Scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── Processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── Tests/
│   ├── conftest.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── Outputs/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── Logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

### Component Responsibilities

* `Scrapers/base_scraper.py` - Shared HTTP/session and request handling.
* `Scrapers/books_scraper.py` - Books to Scrape extraction and pagination.
* `Scrapers/quotes_scraper.py` - Quotes to Scrape extraction and pagination.
* `Processing/cleaning.py` - Data cleaning and normalization.
* `Processing/validation.py` - Validation rules and rejection reasons.
* `Processing/deduplication.py` - Duplicate detection using normalized fingerprints.
* `Tests/` - Unit tests for processing logic.
* `Outputs/` - Generated CSV and JSON files.
* `Logs/` - Execution log.
* `main.py` - Runs the complete pipeline.
* `requirements.txt` - Python dependencies.
* `AI_USAGE.md` - Documentation of AI assistance and verification.

---

## 4. Python Version

The project is developed for Python 3.x.

A Python virtual environment is recommended.

---

## 5. Dependencies

The project uses:

* requests
* beautifulsoup4
* lxml
* pytest

The exact dependencies are listed in `requirements.txt`.

---

## 6. Installation and Setup

Create a virtual environment:

```text
python -m venv venv
```

Activate it on Windows:

```text
venv\Scripts\activate
```

Install dependencies:

```text
pip install -r requirements.txt
```

---

## 7. How to Run

After activating the virtual environment, run:

```text
python main.py
```

This runs the complete pipeline:

```text
Scrape → Clean → Validate → Deduplicate → Consolidate → Save
```

The required output directories are created automatically if they do not already exist.

---

## 8. Pagination

Pagination is implemented by following the websites' `Next` links rather than hard-coding page numbers.

For each source:

1. Start from the main website URL.
2. Fetch the current page.
3. Extract records from the page.
4. Locate the `Next` link.
5. Convert the relative link into an absolute URL.
6. Continue until no `Next` link is available.

During the verified execution:

* Books to Scrape: 50 pages processed, 1,000 records collected.
* Quotes to Scrape: 10 pages processed, 100 records collected.

---

## 9. Data Model

Both sources are normalized into a common structure:

| Field           | Description                                 |
| --------------- | ------------------------------------------- |
| `source`        | Source website name                         |
| `source_url`    | URL associated with the record              |
| `name_or_title` | Book title or quote text                    |
| `category`      | Category when available                     |
| `price`         | Numeric price when applicable               |
| `rating`        | Numeric rating from 1 to 5 when applicable  |
| `author`        | Quote author when applicable                |
| `tags`          | Quote tags when applicable                  |
| `description`   | Description when available                  |
| `scraped_at`    | UTC timestamp when the record was processed |

Fields that are not applicable to a particular source are stored as empty or null values. No information is artificially invented.

---

## 10. Data Cleaning

Cleaning is implemented in `Processing/cleaning.py`.

The cleaning process includes:

* Removing unnecessary leading and trailing whitespace.
* Normalizing text values.
* Converting prices into numeric values.
* Normalizing ratings into numeric values.
* Cleaning tags and text fields.
* Normalizing URLs where required.
* Handling missing values.
* Preserving source-specific fields without inventing missing information.

Cleaning is performed before validation and deduplication.

---

## 11. Data Validation

Validation is implemented in `Processing/validation.py`.

Records are checked for expected data quality, including:

* Required source information.
* Valid-looking URLs.
* Numeric price values where applicable.
* Rating values within the expected range.
* Required title/quote information.
* Recognized source names.
* Missing or invalid values.

Invalid records are rejected rather than causing the entire pipeline to fail.

The summary report records rejected counts and rejection reasons.

---

## 12. Deduplication

Deduplication is implemented in `Processing/deduplication.py`.

Exact string comparison alone is not used.

Before generating a fingerprint, the relevant fields are normalized by:

1. Converting text to lowercase.
2. Removing punctuation.
3. Normalizing whitespace.
4. Combining source-specific identifying fields.
5. Generating a SHA-256 fingerprint.

For Books to Scrape, the fingerprint uses:

```text
source + book title
```

For Quotes to Scrape, the fingerprint uses:

```text
source + author + first 50 characters of quote text
```

The first occurrence is retained and subsequent matching records are treated as duplicates.

During the verified execution, 1 duplicate was detected and removed.

---

## 13. Error Handling and Logging

The scraper includes logging and error handling for common scraping problems, including:

* HTTP request failures.
* Connection errors.
* Timeout errors.
* Unexpected page structures.
* Missing HTML elements.
* Invalid values.
* Pagination problems.

Problems are logged and the pipeline is designed to continue where possible instead of terminating unnecessarily.

Execution logs are stored in:

```text
Logs/scraper.log
```

---

## 14. Test Coverage

Unit tests are provided for the processing components.

Tests cover:

* Data cleaning.
* Validation.
* Deduplication.

The test suite was executed successfully with:

```text
pytest -q
```

Result:

```text
8 tests passed
```

The tests do not depend on live website access.

---

## 15. Output Files

The pipeline generates:

### `Outputs/final_dataset.csv`

Contains the consolidated, cleaned, validated, and deduplicated records from both websites.

Verified result:

```text
Books to Scrape: 999 final records
Quotes to Scrape: 100 final records
Total final records: 1,099
```

The CSV contains 1,100 lines in total:

```text
1 header + 1,099 data records
```

### `Outputs/summary_report.json`

Contains execution metrics including:

* Records collected per source.
* Records remaining after cleaning.
* Rejected record count.
* Rejection reasons.
* Duplicate count.
* Final record count.
* Start time.
* End time.
* Execution duration.
* Reconciliation result.

Verified summary:

```text
Books collected: 1000
Quotes collected: 100
Total collected: 1100
Rejected: 0
Duplicates removed: 1
Final records: 1099
Reconciliation: true
Execution time: 85.65 seconds
```

### `Logs/scraper.log`

Contains timestamped execution information, including requests, pagination progress, warnings, and errors.

---

## 16. Reconciliation

The final dataset is reconciled against the processing metrics.

For the verified execution:

```text
Total collected = 1,100
Rejected = 0
Duplicates = 1

1,100 - 0 - 1 = 1,099
```

The final CSV contains:

```text
1,099 records
```

Therefore:

```text
Reconciliation = true
```

---

## 17. Assumptions

* The websites are publicly accessible scraping practice websites.
* Website HTML structure and selectors are assumed to remain compatible with the implementation.
* Ratings are expected to be within the range of 1 to 5.
* Prices are converted to numeric values where applicable.
* Fields that do not apply to a source are left empty or null.
* Duplicate detection is based on normalized identifying fields rather than exact complete-record comparison.
* The scraper processes the pages available at execution time.

---

## 18. Limitations

* Website HTML changes could require selector updates.
* The scraper is designed specifically for the two assignment websites.
* It does not bypass CAPTCHA, authentication, or other access restrictions.
* Duplicate detection is rule-based and may not identify every possible semantic duplicate.
* The final results depend on the data available on the websites at the time of execution.

---

## 19. AI Usage

AI assistance was used during development for:

* Understanding the assignment requirements.
* Planning the project structure.
* Discussing scraping and pagination approaches.
* Reviewing cleaning, validation, and deduplication logic.
* Troubleshooting errors.
* Improving documentation.

All AI-assisted code and suggestions were reviewed, tested, and adjusted before being included in the final project.

Detailed AI usage information is documented separately in:

```text
AI_USAGE.md
```

---

## 20. Final Verification

The complete pipeline was executed successfully using:

```text
python main.py
```

Verified result:

```text
Books to Scrape records: 1000
Quotes to Scrape records: 100
Rejected records: 0
Duplicates removed: 1
Final records: 1099
Reconciliation: true
Execution time: 85.65 seconds
```

The unit test suite also passed successfully:

```text
8 tests passed
```

The project therefore produces the required dataset, summary report, logs, tests, and documentation.
