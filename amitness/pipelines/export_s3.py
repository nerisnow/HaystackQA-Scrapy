from s3pipeline.pipelines import S3Pipeline
from overrides import overrides


class S3Writer(S3Pipeline):

    def __init__(self,settings, stats):
        self.id=None
        super().__init__(settings, stats)

    @overrides
    def process_item(self, item, spider):
        """
        Process single item. Add item to items and then upload to S3/GCS
        if size of items >= max_chunk_size.
        """
        # self.id = None
        self._timer_cancel()

        self.items.append(item)
        if len(self.items) >= self.max_chunk_size:
            self._upload_chunk()
        
        self.id = item["meta"]["title"]
        self._timer_start()

        return item

    @overrides
    def _get_uri_params(self):
        params = {}
        for key in dir(self._spider):
            params[key] = getattr(self._spider, key)

        params['chunk'] = self.id
        params['time'] = self.ts
        return params