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
