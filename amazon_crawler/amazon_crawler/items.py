# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from dataclasses import dataclass
import datetime


@dataclass
class AmazonCrawlerItem:
    rank: int = None
    name: str = None
    price: str = None
    url: str = None
    dtime: datetime = None
    
    def to_json(self): 
        
        body = {
            "rank": self.rank,
            "name": self.name,
            "price": self.price,
            "url": self.url,
            "dtime": self.dtime
        }

        return body

@dataclass
class AmazonProductDetail:
    title: str = None
    new_price: str = None
    last_price: str = None
    rating: str = None
    rating_count: str = None
    main_img_url: str = None
    dtime: datetime = None

    def to_json(self): 
        
        body = {
            "title": self.title,
            "new_price": self.new_price,
            "last_price": self.last_price,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "main_img_url": self.main_img_url,
            "dtime": self.dtime
        }

        return body