from urllib.parse import urljoin

from bs4 import BeautifulSoup

from Scrapers.base_scraper import BaseScraper


class QuotesScraper(BaseScraper):

    START_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.START_URL

        while current_url:

            html = self.fetch_page(current_url)

            if html is None:
                break

            soup = BeautifulSoup(html, "lxml")

            quotes = soup.select("div.quote")

            for quote in quotes:
                try:
                    text_element = quote.select_one("span.text")
                    author_element = quote.select_one("small.author")
                    tag_elements = quote.select("a.tag")

                    # Get quote text
                    quote_text = (
                        text_element.get_text(strip=True)
                        if text_element
                        else ""
                    )

                    # Get author
                    author = (
                        author_element.get_text(strip=True)
                        if author_element
                        else ""
                    )

                    # Get tags
                    tags = [
                        tag.get_text(strip=True)
                        for tag in tag_elements
                    ]

                    # Create common record structure
                    record = {
                        "source": "Quotes to Scrape",
                        "source_url": current_url,
                        "name_or_title": quote_text,
                        "category": "",
                        "price": "",
                        "rating": "",
                        "author": author,
                        "tags": ";".join(tags),
                        "description": "",
                    }

                    records.append(record)

                except Exception as error:
                    print(f"Could not process a quote: {error}")

            # Follow the website's "next" link
            next_link = soup.select_one("li.next > a")

            if next_link:
                current_url = urljoin(
                    current_url,
                    next_link.get("href", "")
                )
            else:
                current_url = None

        return records