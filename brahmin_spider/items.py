# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BrahminSpiderItem:
    product_name: Optional[str] = field(default=None)
    product_id: Optional[str] = field(default=None)
    link: Optional[str] = field(default=None)
    designer: Optional[str] = field(default=None)
    color: Optional[str] = field(default=None)
    price: Optional[float] = field(default=None)
    sale_price: Optional[float] = field(default=None)
    stock_status: Optional[str] = field(default=None)
    image_urls: Optional[list] = field(default=None)
    description: Optional[str] = field(default=None)
    raw_description: Optional[str] = field(default=None)

# from scrapy.item import Item, Field
#
#
# class BrahminSpiderItem(Item):
#     product_name = Field()
#     product_id = Field()
#     link = Field()
#     designer = Field()
#     color = Field()
#     price = Field()
#     sale_price = Field()
#     stock_status = Field()
#     image_urls = Field()
#     description = Field()
#     raw_description = Field()
