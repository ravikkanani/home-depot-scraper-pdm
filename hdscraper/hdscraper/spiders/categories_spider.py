"""
Scrapy crawl spider class that goes to the site map page
and extracts all category names and links.
"""

import re

import scrapy
from database import DatabaseWriter
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import HdscraperCategoryItem


class CategoryCrawler(CrawlSpider):
    """
    Scrapy crawler class that goes to the site map page and extracts all
    category links.
    """

    name = "category_crawler"
    allowed_domains = ["homedepot.com"]
    start_urls = ["https://www.homedepot.com/c/site_map"]

    rules = (
        Rule(
            LinkExtractor(
                deny=(r"\n\t\t\t\t\t\t\t", r"^\/b"),
                restrict_xpaths=("//div[@class='content experience']",),
            ),
            callback="parse_category",
            follow=False,
        ),
    )

    item = HdscraperCategoryItem(map)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()
        self.db_writer = DatabaseWriter(hd_products.db)

    def parse_category(self, response):
        """Parse category links."""
        for link in response.css("a[href*='https://www.homedepot.com/b/']"):
            if not re.match(
                r"https://www\.homedepot\.com/b/[^/]+/N-[a-zA-Z0-9]+/?$",
                link.attrib["href"],
            ):
                continue
            category_link = link.css("::attr(href)").get()
            if category_link not in self.seen_urls:
                self.seen_urls.add(category_link)
                if link.css("::text").get().strip():
                    data {
                        "category": link.css("::text").get().strip(),
                        "url": category_link,
                    }

                    self.db_writer.write_category(data)
        self.db_writer.close()
