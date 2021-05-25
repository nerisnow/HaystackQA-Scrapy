# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import Join, TakeFirst
from scrapy import Field, Item

class CustomField(Field):
    def __init__(self):
        super().__init__(output_processor=TakeFirst())


class BlogItem(Item):
    # Scraped fields
    title = CustomField()
    # duration = CustomField()
    content = Field(output_processor=Join())

    # Housekeeping Fields
    project = CustomField()
    spider = CustomField()
    server = CustomField()
    date = CustomField()
    
