import pymongo
from wayfair import settings
from wayfair.utils.config import *

class WayfairBestSellerPipeline:
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
        # pass
        try:
            self.collection.insert_one(item)
        except Exception as e:
            raise Exception("Cannot update item to the database", e)