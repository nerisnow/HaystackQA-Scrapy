import json

from itemadapter import ItemAdapter

class JsonWriterPipeline:
    """
    Pipeline to save the scraped data in a json lines file
    """

    def open_spider(self, spider):
        self.file = open('blogs.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

