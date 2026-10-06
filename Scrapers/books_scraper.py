from urllib.parse import urljoin

from bs4 import BeautifulSoup

from Scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):

    START_URL = "https://books.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.START_URL

        while current_url:

            html = self.fetch_page(current_url)

            if html is None:
                break

            soup = BeautifulSoup(html, "lxml")

            books = soup.select("article.product_pod")

            for book in books:
                try:
                    title_element = book.select_one("h3 > a")
                    price_element = book.select_one("p.price_color")
                    rating_element = book.select_one("p.star-rating")

                    # Get book title
                    title = (
                        title_element.get("title", "").strip()
                        if title_element
                        else ""
                    )

                    # Get price
                    price = (
                        price_element.get_text(strip=True)
                        if price_element
                        else ""
                    )

                    # Get rating word
                    rating = ""

                    if rating_element:
                        classes = rating_element.get("class", [])

                        for class_name in classes:
                            if class_name != "star-rating":
                                rating = class_name
                                break

                    # Get book URL
                    book_link = (
                        title_element.get("href", "")
                        if title_element
                        else ""
                    )

                    book_url = urljoin(current_url, book_link)

                    # Create common record structure
                    record = {
                        "source": "Books to Scrape",
                        "source_url": book_url,
                        "name_or_title": title,
                        "category": "",
                        "price": price,
                        "rating": rating,
                        "author": "",
                        "tags": "",
                        "description": "",
                    }

                    records.append(record)

                except Exception as error:
                    print(f"Could not process a book: {error}")

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