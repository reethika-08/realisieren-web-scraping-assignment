import csv
import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

from Scrapers.books_scraper import BooksScraper
from Scrapers.quotes_scraper import QuotesScraper
from Processing.cleaning import clean_text, clean_price, clean_rating
from Processing.validation import validate_record
from Processing.deduplication import find_duplicates


# -----------------------------
# File locations
# -----------------------------

OUTPUT_DIR = Path("Outputs")
LOG_DIR = Path("Logs")

CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
SUMMARY_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


# -----------------------------
# Common CSV columns
# -----------------------------

COLUMNS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


# -----------------------------
# Logging setup
# -----------------------------

def setup_logging():
    """
    Configure logging to write to both
    the terminal and scraper.log.
    """

    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# -----------------------------
# Cleaning
# -----------------------------

def clean_record(record):
    """
    Clean text fields and convert price/rating
    into the required formats.
    """

    record["source"] = clean_text(record.get("source"))
    record["source_url"] = clean_text(record.get("source_url"))
    record["name_or_title"] = clean_text(record.get("name_or_title"))
    record["category"] = clean_text(record.get("category"))
    record["author"] = clean_text(record.get("author"))
    record["tags"] = clean_text(record.get("tags"))
    record["description"] = clean_text(record.get("description"))

    if record["source"] == "Books to Scrape":
        record["price"] = clean_price(record.get("price"))
        record["rating"] = clean_rating(record.get("rating"))
    else:
        record["price"] = None
        record["rating"] = None

    # Add timestamp showing when the record was scraped
    if not record.get("scraped_at"):
        record["scraped_at"] = datetime.now(
            timezone.utc
        ).isoformat()

    return record


# -----------------------------
# Save CSV
# -----------------------------

def save_csv(records):
    """
    Save final cleaned records to CSV.
    """

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS
        )

        writer.writeheader()
        writer.writerows(records)


# -----------------------------
# Save summary JSON
# -----------------------------

def save_summary(stats):
    """
    Save scraping statistics to JSON.
    """

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        SUMMARY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            stats,
            file,
            indent=4
        )


# -----------------------------
# Main ETL process
# -----------------------------

def main():

    setup_logging()

    start_time = time.time()
    start_timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    logging.info("Starting scraping assignment")

    # ---------------------------------
    # 1. SCRAPE BOOKS
    # ---------------------------------

    logging.info("Scraping Books to Scrape")

    try:
        books = BooksScraper().scrape()

        logging.info(
            "Books collected: %d",
            len(books)
        )

    except Exception as error:

        logging.error(
            "Books scraping failed: %s",
            error
        )

        books = []

    # ---------------------------------
    # 2. SCRAPE QUOTES
    # ---------------------------------

    logging.info("Scraping Quotes to Scrape")

    try:
        quotes = QuotesScraper().scrape()

        logging.info(
            "Quotes collected: %d",
            len(quotes)
        )

    except Exception as error:

        logging.error(
            "Quotes scraping failed: %s",
            error
        )

        quotes = []

    # ---------------------------------
    # 3. CONSOLIDATE RAW DATA
    # ---------------------------------

    raw_records = books + quotes

    logging.info(
        "Total raw records: %d",
        len(raw_records)
    )

    # ---------------------------------
    # 4. CLEAN DATA
    # ---------------------------------

    logging.info("Cleaning data")

    cleaned_records = []

    for record in raw_records:
        try:
            cleaned_record = clean_record(record)
            cleaned_records.append(cleaned_record)

        except Exception as error:
            logging.error(
                "Could not clean record: %s | Error: %s",
                record.get("name_or_title", ""),
                error
            )

    logging.info(
        "Records after cleaning: %d",
        len(cleaned_records)
    )

    # ---------------------------------
    # 5. VALIDATE DATA
    # ---------------------------------

    logging.info("Validating data")

    valid_records = []

    rejected = 0
    rejected_by_reason = {}

    for record in cleaned_records:

        problems = validate_record(record)

        if problems:

            rejected += 1

            for problem in problems:
                rejected_by_reason[problem] = (
                    rejected_by_reason.get(problem, 0) + 1
                )

            logging.warning(
                "Rejected record: %s | Reasons: %s",
                record.get("name_or_title", ""),
                ", ".join(problems)
            )

        else:
            valid_records.append(record)

    logging.info(
        "Rejected records: %d",
        rejected
    )

    # ---------------------------------
    # 6. REMOVE DUPLICATES
    # ---------------------------------

    logging.info("Removing duplicates")

    unique_records, duplicates = find_duplicates(
        valid_records
    )

    logging.info(
        "Duplicates detected: %d",
        len(duplicates)
    )

    # ---------------------------------
    # 7. SAVE FINAL CSV
    # ---------------------------------

    logging.info("Saving final CSV")

    save_csv(unique_records)

    # ---------------------------------
    # 8. CREATE SUMMARY
    # ---------------------------------

    duration = round(
        time.time() - start_time,
        2
    )

    end_timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    stats = {

        "collected_per_source": {
            "Books to Scrape": len(books),
            "Quotes to Scrape": len(quotes)
        },

        "after_cleaning_per_source": {
            "Books to Scrape": sum(
                1
                for record in cleaned_records
                if record["source"] == "Books to Scrape"
            ),

            "Quotes to Scrape": sum(
                1
                for record in cleaned_records
                if record["source"] == "Quotes to Scrape"
            )
        },

        "rejected_count": rejected,

        "rejected_by_reason": rejected_by_reason,

        "duplicates_detected": len(duplicates),

        "final_record_count": len(unique_records),

        "start_time": start_timestamp,

        "end_time": end_timestamp,

        "duration_seconds": duration,

        "reconciliation": (
            len(raw_records)
            - rejected
            - len(duplicates)
            == len(unique_records)
        )
    }

    # ---------------------------------
    # 9. SAVE SUMMARY JSON
    # ---------------------------------

    logging.info("Saving summary report")

    save_summary(stats)

    # ---------------------------------
    # 10. FINAL RESULT
    # ---------------------------------

    logging.info("Scraping completed")

    print("\n" + "=" * 50)
    print("SCRAPING COMPLETED")
    print("=" * 50)

    print(f"Books collected       : {len(books)}")
    print(f"Quotes collected      : {len(quotes)}")
    print(f"Total raw records     : {len(raw_records)}")
    print(f"Rejected records      : {rejected}")
    print(f"Duplicates detected   : {len(duplicates)}")
    print(f"Final records         : {len(unique_records)}")
    print(f"Duration              : {duration} seconds")
    print(f"Reconciliation        : {stats['reconciliation']}")

    print("\nOutput files:")
    print(f"CSV     : {CSV_FILE}")
    print(f"Summary : {SUMMARY_FILE}")
    print(f"Log     : {LOG_FILE}")

    print("=" * 50)


# -----------------------------
# Run program
# -----------------------------

if __name__ == "__main__":
    main()