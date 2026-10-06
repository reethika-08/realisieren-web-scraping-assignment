# AI Usage

## Overview

AI tools were used during the development of this scraping assignment for guidance, debugging, code explanation, testing support, and documentation.

## AI Tool Used

**Tool:** ChatGPT

## How AI Was Used

ChatGPT was used for:

* Understanding the assignment requirements and ETL workflow.
* Designing the Python project structure.
* Understanding web scraping using `requests` and `BeautifulSoup`.
* Understanding HTML selectors and pagination.
* Debugging Python import and testing issues.
* Improving data cleaning and validation logic.
* Designing duplicate-detection logic.
* Creating and improving unit tests using `pytest`.
* Reviewing error handling and logging.
* Preparing and reviewing project documentation.
* Explaining implementation decisions and interview questions.

## Representative Prompts

Examples of prompts used during development include:

1. "Help me create a Python web scraping project structure for two different public websites and consolidate the data into a common schema."

2. "How can I implement pagination by following the Next link instead of hard-coding page URLs?"

3. "Help me create cleaning, validation, and deduplication functions for scraped records."

4. "Why is pytest showing an import error in my project, and how can I fix the project imports?"

5. "Review my scraping assignment implementation against the provided requirements and identify any missing or necessary improvements."

## AI-Assisted Parts

AI assistance was used in the following areas:

* Initial project structure and module organization.
* Scraper implementation guidance for Books to Scrape and Quotes to Scrape.
* Pagination logic.
* Common record/schema design.
* Data cleaning functions.
* Validation rules.
* Duplicate fingerprinting and deduplication.
* Unit test structure.
* Error handling and logging improvements.
* README and AI usage documentation.

## Important Changes After Reviewing AI Output

AI-generated suggestions were reviewed and tested locally before being included.

During review:

* Import and pytest issues were identified and fixed using a `Tests/conftest.py` file.
* Scraped price values required cleaning because the website response/display could contain encoding artifacts.
* Rating words such as "Three" were converted into numeric values.
* The duplicate-detection logic was designed to normalize whitespace, capitalization, and punctuation before generating fingerprints.
* A suggested approach for assigning book categories from the listing-page breadcrumb was rejected because the page-level category could incorrectly be applied to individual books. The implementation therefore avoids inventing category values.
* The final implementation was kept simple and focused on the assignment requirements rather than adding unnecessary technologies.

## Incorrect or Incomplete AI Suggestions Discovered

One AI-generated suggestion proposed using the listing page's breadcrumb to populate the category field for every book on that page. This was identified as potentially inaccurate because the breadcrumb represents the page/category context and should not automatically be treated as the category of every individual record.

The approach was not used in the final implementation.

## Human Understanding

The final implementation was reviewed and tested manually. The developer understands the main components of the solution, including:

* HTTP requests and response handling.
* Retry behavior for failed requests.
* HTML parsing with BeautifulSoup.
* Following pagination through the website's Next link.
* Data cleaning and normalization.
* Numeric price conversion.
* Rating normalization.
* Record validation and rejection.
* Duplicate detection using normalized fingerprints.
* Consolidation of records from multiple sources.
* CSV and JSON output generation.
* Logging.
* Unit testing with pytest.

## Testing and Verification

The project was tested locally using:

```text
pytest -q
```

Test result:

```text
8 passed
```

The complete scraping pipeline was also executed using:

```text
python main.py
```

The successful execution collected:

* 1,000 Books to Scrape records.
* 100 Quotes to Scrape records.
* 1,100 total raw records.
* 0 rejected records.
* 1 duplicate detected and removed.
* 1,099 final records.

The final CSV, summary JSON, and scraper log were checked after execution.

## AI Limitations

AI-generated suggestions were treated as development guidance rather than blindly copied. The code was reviewed, tested locally, and modified when necessary to match the actual website structures and assignment requirements.

The final implementation remains the responsibility of the developer, who can explain the main design and implementation decisions during an interview.
