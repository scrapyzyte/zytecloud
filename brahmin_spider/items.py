# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BrahminSpiderItem(scrapy.Item):
    product_name = scrapy.Field()
    product_id = scrapy.Field()
    link = scrapy.Field()
    designer = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
    stock_status = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    raw_description = scrapy.Field()
