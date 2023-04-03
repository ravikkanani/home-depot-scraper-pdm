"""Spider to scrape Home Depot product data using a GUI where the user can select categories"""

import sqlite3
import tkinter as tk

import scrapy
from hdscraper.items import HdscraperProductItems
from scrapy.crawler import CrawlerProcess


class ProductSpider(scrapy.Spider):
    """
    Scrapy spider class that defines the behavior of the spider for scraping
    product data from the Home Depot website.
    """

    name = "detailsspider"

    def start_requests(self):
        urls = []
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"myarg": "value"})

    def parse(self, response):
        for product_url in response.css("a.product::attr(href)").getall():
            yield scrapy.Request(url=product_url, callback=self.parse_product)

    def parse_product(self, response):
        product = {}
        product["title"] = response.css("h1.product-title::text").get().strip()
        product["price"] = response.css("span.price::text").get().strip()
        # Add more fields as needed
        yield product


def hello_ken():
    print("hello Ken 2")


def start_scrapy(categories):
    urls = []
    for category in categories:
        urls.append(f"https://www.homedepot.com/sitemap/{category}")
    process = CrawlerProcess(
        {
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "FEED_FORMAT": "json",
            "FEED_URI": "output.json",
            "START_URLS": urls,
        }
    )
    process.crawl(HomeDepotSpider)
    process.start()


def on_button_click():
    categories = []
    for i in range(len(category_vars)):
        if category_vars[i].get() == 1:
            categories.append(categories_list[i])
    start_scrapy(categories)


def get_categories():
    open_db = sqlite3.connect("hdscraper2.db")
    cursor = open_db.cursor()
    categories = cursor.execute("SELECT category FROM categories")
    categories = [category[0] for category in categories]
    
    return categories


def gui():
    # Create GUI
    root = tk.Tk()
    root.title("Home Depot Scraper")
    categories_list = get_categories()

    category_vars = []
    for category in categories_list:
        category_vars.append(tk.IntVar(value=0))
    for i in range(len(categories_list)):
        tk.Checkbutton(root, text=categories_list[i], variable=category_vars[i]).grid(
            row=i, column=0
        )

    tk.Button(root, text="Scrape", command=on_button_click).grid(
        row=len(categories_list), column=0
    )
    print("Hello world")
    root.mainloop()


gui()