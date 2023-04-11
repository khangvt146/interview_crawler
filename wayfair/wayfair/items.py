from dataclasses import dataclass
import datetime

@dataclass
class WayfairProductDetail:
    title: str = None
    brand: str = None
    new_price: str = None
    last_price: str = None
    rating: str = None
    rating_count: str = None
    shipping_fee: str = None
    sponsored: bool = None
    dtime: datetime = None

    def to_json(self): 
        
        body = {
            "title": self.title,
            "brand": self.brand,
            "new_price": self.new_price,
            "last_price": self.last_price,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "shipping_fee": self.shipping_fee,
            "sponsored": self.sponsored,
            "dtime": self.dtime
        }

        return body