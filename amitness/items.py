# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from bs4 import BeautifulSoup
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy import Field, Item


def filter_text(value: str) -> str:
    """Extracts all article paragraphs and removes encoding"""
    soup = BeautifulSoup(value, "lxml")
    if soup.find_all("p"):
        text = soup.get_text()
        text_encode = text.encode("ascii", "ignore")
        text_decode = text_encode.decode()
        return text_decode


class CustomField(Field):
    def __init__(self):
        super().__init__(output_processor=TakeFirst())


class MetaItem(Item):
    name = CustomField()


class BlogItem(Item):
    text = Field(input_processor=MapCompose(filter_text), output_processor=Join())
    meta = CustomField()

    # # Housekeeping Fields
    # project = CustomField()
    # spider = CustomField()
    # server = CustomField()
    # date = CustomField()
