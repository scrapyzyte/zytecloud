# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class BrahminSpiderItem(Item):
    product_name = Field()
    product_id = Field()
    link = Field()
    designer = Field()
    color = Field()
    price = Field()
    sale_price = Field()
    stock_status = Field()
    image_urls = Field()
    description = Field()
    raw_description = Field()
