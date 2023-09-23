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
    stock_status: Optional[bool] = field(default=None)
    image_urls: Optional[list] = field(default=None)
    description: Optional[str] = field(default=None)
    raw_description: Optional[list] = field(default=None)


# from scrapy import Field, Item
#
#
# # Serializer:
# # Purpose: A serializer in Scrapy is used to convert scraped data into a specific format.
# # This format can be JSON, XML, or any other format that you want to use to store or export the scraped data.
# #
# # Usage: You typically use serializers to define how the data should be structured and formatted before
# # it is stored or exported. For example, you might want to serialize scraped items into JSON for storage
# # in a database or for further analysis.
# #
# # Implementation: Serializers are implemented as Python classes that you define in your Scrapy project.
# # You specify the serialization format and the data transformation rules within these classes.
# #
# # In Scrapy, you can use a custom item serializer in conjunction with a default item exporter,
# # but you'll need to configure your Scrapy project appropriately to make this work.
# # The default item exporter in Scrapy is typically used to export scraped data items to
# # various formats like JSON, CSV, or XML. However, the default item exporter doesn't support
# # custom serialization logic out of the box.
# def serialize_price(value):
#     return f"$ {str(value)}"
#
#
# class BrahminSpiderItem(Item):
#     product_name = Field()
#     product_id = Field()
#     link = Field()
#     designer = Field()
#     color = Field()
#     price = Field(serializer=serialize_price)
#     sale_price = Field()
#     stock_status = Field()
#     image_urls = Field()
#     description = Field()
#     raw_description = Field()
