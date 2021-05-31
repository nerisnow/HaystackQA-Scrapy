import os
import boto3
import traceback


ACCESS_KEY=os.environ.get('ACCESS_KEY')
SECRET_KEY=os.environ.get('SECRET_KEY')
BUCKET=os.environ.get('BUCKET')

class S3Writer(object):
    """
    Pipeline to save the scraped data as s3 objects
    """
    def __init__(self):
        self.ACCESS_KEY =ACCESS_KEY
        self.SECRET_KEY = SECRET_KEY
        self.Bucket = BUCKET
        self.client = boto3.client("s3", aws_access_key_id=self.ACCESS_KEY, aws_secret_access_key=self.SECRET_KEY)
        
    def process_item(self, item, spider):
        id = str(item['meta']['id'])
        try:
            self.client.put_object(ACL="private", Body=item['text'], Bucket=self.Bucket, Key=f"article/{id}.txt")
        except Exception as e:
            print(e)
        finally:
            return item

    