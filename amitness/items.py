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

class MetaItem(Item):
    # Scraped fields
    name = Field()

class BlogItem(Item):
    # duration = CustomField()
    text = Field(output_processor=Join())
    meta  = Field(serializer=MetaItem)

    # # Housekeeping Fields
    # project = CustomField()
    # spider = CustomField()
    # server = CustomField()
    # date = CustomField()
    
