import time
import logging
import requests


class BaseScraper:
    def __init__(self):
        self.session = requests.Session()
        self.delay = 0.5
        self.timeout = 10

    def fetch_page(self, url):
        for attempt in range(3):
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout
                )

                response.raise_for_status()

                logging.info(
                    "Successfully fetched: %s",
                    url
                )

                time.sleep(self.delay)

                return response.text

            except requests.RequestException as error:
                logging.error(
                    "Request failed (attempt %d/3) for %s: %s",
                    attempt + 1,
                    url,
                    error
                )

                if attempt == 2:
                    logging.error(
                        "Giving up after 3 attempts: %s",
                        url
                    )
                    raise

                time.sleep(1)