import socket
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from amitness.items import BlogItem, MetaItem


class BlogSpider(scrapy.Spider):
    name = "blog"
    allowed_domains = ["amitness.com"]

    BASE_URL = "https://amitness.com"

    def start_requests(self):
        yield scrapy.Request(url=self.BASE_URL, callback=self.parse_topics)

    def parse_topics(self, response):
        """Parse the list of blogs from the webiste"""
        paths = response.css("div.entries-list div.list__item a::attr(href)").getall()
        print(paths)
        for path in paths:
            path_url = f"{self.BASE_URL}{path}"
            yield scrapy.Request(url=path_url, callback=self.parse)

        next_url = [
            m.css("a::attr(href)").get()
            for m in response.css("nav.pagination a")
            if m.css("a::text").get() == "Next"
        ]

        if next_url:
            url = f"{self.BASE_URL}{next_url[0]}"
            yield scrapy.Request(url=url, callback=self.parse_topics)
        else:
            print("No next blog found")

    def parse(self, response):
        """Parse a single blog from the list of blogs"""
        bl = ItemLoader(item=BlogItem(), response=response)
        content = response.css("section.page__content")

        # adding value to the item containers
        bl.add_value("text", content.css("p::text").getall())
        bl.add_value("meta", self.get_meta(response))
        return bl.load_item()

    def get_meta(self, response):
        ml = ItemLoader(item=MetaItem(), response=response)
        ml.add_value("name", response.css("title::text").get())
        return ml.load_item()


# saving as text files
# filename = f"./data/{title}.txt"
# blog_text = ''.join(content.css("p::text").extract())
# with open(filename, 'a') as f:
#     f.write(blog_text)
