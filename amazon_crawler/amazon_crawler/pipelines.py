import pymongo
from amazon_crawler import settings
# from scrapy.exceptions import DropItem
from amazon_crawler.utils.config import *

class AmazonBestSellerPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authSource="admin"
        )
        db = connection[settings.MONGO_DB]
        self.collection = db[settings.BEST_SELLER_MONGO_COLLECTION]

    def process_item(self, item, spider):
        try:
            self.collection.insert_one(item)
        except Exception as e:
            raise Exception("Cannot update item to the database", e)
        

class AmazonProductDetailPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authSource="admin"
        )
        db = connection[settings.MONGO_DB]
        self.collection = db[settings.PRODUCT_DETAILS_MONGO_COLLECTION]

    def process_item(self, item, spider):
        try:
            self.collection.insert_one(item)
        except Exception as e:
            raise Exception("Cannot update item to the database", e)
            