import socket
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from amitness.items import BlogItem


class BlogSpider(scrapy.Spider):
    name  = "blog"
    allowed_domains = ["amitness.com"]

    BASE_URL = "https://amitness.com"
    def start_requests(self):
        yield scrapy.Request(url=self.BASE_URL, callback= self.parse_topics)

    def parse_topics(self, response):
        """ Parse the list of blogs from the webiste
        """
        # filename  = 'amitness_blog.html'

        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        paths = response.css("div.entries-list div.list__item a::attr(href)").getall()
        print(paths)
        for path in paths:
            path_url = f"{self.BASE_URL}{path}"
            print(path)
            # path_url = response.urljoin(path)
            yield scrapy.Request(
                url = path_url, callback=self.parse
            )

        # for m in response.css("nav.pagination a"):
        #     if m.css("a::text").get()=="Next":
        #         href = m.css("a::attr(href)").get() 
        #         print(href)
        
        next_url = [m.css("a::attr(href)").get() for m in response.css("nav.pagination a") if m.css("a::text").get()=="Next"]
        
        if next_url:
            url = f"{self.BASE_URL}{next_url[0]}"
            # url = response.urljoin(next_url[0])
            print(url)
            yield scrapy.Request(
                url=url, callback=self.parse_topics)

        else:
            print("No next blog found")
        

    def parse(self, response):
        """ Parse a single blog from the list of blogs
        """
        title = response.css("title::text").get()
        filename = f"./data/{title}.txt"
        bl = ItemLoader(item = BlogItem(), response=response)
        content = response.css("section.page__content")
        
        bl.add_value("title", response.css("title::text").get())
        # bl.add_value("duration", response.css(".page__meta-readtime::text").getall())
        bl.add_value("content", content.css("p::text").getall())

        bl.add_value("project", self.settings.get("BOT_NAME"))
        bl.add_value("spider", self.name)
        bl.add_value("server", socket.gethostname())
        bl.add_value("date", datetime.now())

        blog_text = ''.join(content.css("p::text").extract())
        with open(filename, 'a') as f:
            f.write(blog_text)

        return bl.load_item()
        





