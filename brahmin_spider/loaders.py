import html
from abc import ABC, abstractmethod

import html2text
from itemloaders.processors import Compose, Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from brahmin_spider.items import BrahminSpiderItem


def escape_html(text):
    """Escape HTML entities e.g. replace &gt; with >"""
    return html.unescape(text)


def strip_html(html_text):
    """Strips html tags out of a string."""
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text = text_maker.handle(html_text)
    return text


def validate_string(value):
    if not isinstance(value, str):
        raise ValueError("Field must be type str!")
    return value


def validate_float(value):
    if not isinstance(value, float):
        raise ValueError("Field must be type float!")
    return value


def validate_boolean(value):
    if not isinstance(value, bool):
        raise ValueError("Field must be type boolean!")
    return value


def validate_list(value):
    if not isinstance(value, list):
        raise ValueError("Field must be type list!")
    return value


class DataLoader(ABC):
    @abstractmethod
    def add_item_prices(self, product):
        pass

    @abstractmethod
    def add_item_images(self, product):
        pass


class ProductLoader(DataLoader, ItemLoader):
    default_item_class = BrahminSpiderItem  # Specify the item class for this loader

    product_name_in = MapCompose(validate_string)
    product_id_in = MapCompose(validate_string)
    link_in = MapCompose(validate_string)
    designer_in = MapCompose(validate_string)
    color_in = MapCompose(validate_string)
    price_in = MapCompose(validate_float)
    sale_price_in = MapCompose(validate_float)
    stock_status_in = MapCompose(validate_boolean)
    image_urls_in = MapCompose(validate_list)
    description_in = MapCompose(validate_string, escape_html, strip_html)

    product_name_out = Join()

    def add_item_prices(self, product):
        price_data = product["price"]

        sale_price = float(0.00)

        if price_data.get("list"):
            price = float(price_data["list"]["value"])
            sale_price = float(price_data["sales"]["value"])
        else:
            price = float(price_data["sales"]["value"]) or float(price_data["min"]["sales"]["value"])

        self.add_value("price", price)
        self.add_value("sale_price", sale_price)

    def add_item_images(self, product):
        self.add_value("image_urls", [i["absURL"] for i in product["images"]["hi-res"]])
