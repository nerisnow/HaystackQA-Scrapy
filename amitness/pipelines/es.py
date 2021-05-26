from elasticsearch import Elasticsearch
from scrapy.exceptions import NotConfigured


class EsWriter(object):
    """A pipeline that writes to Elastic Search"""

    @classmethod
    def from_crawler(cls, crawler):
        es_url = crawler.settings.get("ES_PIPELINE_URL", None)

        if not es_url:
            raise NotConfigured

        return cls(es_url)

    def __init__(self, es_url):
        self.es_url = es_url
        self.index = "amitness_blogs"

    def open_spider(self, spider):
        self.client = Elasticsearch(self.es_url)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            res = self.client.index(index=self.index, id=item["title"], body=dict(item))
        except Exception as e:
            print(e)
        finally:
            return item
