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


def validate_product_name(value):
    if not value:
        raise ValueError("Field product_name is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field product_name must be str")
    return value


def validate_product_id(value):
    if not value:
        raise ValueError("Field product_id is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field product_id must be str")
    return value


def validate_link(value):
    if not value:
        raise ValueError("Field link is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field link must be str")
    return value


def validate_designer(value):
    if not value:
        raise ValueError("Field designer is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field designer must be str")
    return value


def validate_color(value):
    if not value:
        raise ValueError("Field color is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field color must be str")
    return value


def validate_price(value):
    if not value:
        raise ValueError("Field price is empty.")
    elif not isinstance(value, float):
        raise ValueError("Field price must be float")
    return value


def validate_sale_price(value):
    if not value:
        raise ValueError("Field sale_price is empty.")
    elif not isinstance(value, float):
        raise ValueError("Field sale_price must be float")
    return value


def validate_stock_status(value):
    if not value:
        raise ValueError("Field stock_status is empty.")
    elif not isinstance(value, bool):
        raise ValueError("Field stock_status must be boolean")
    return value


def validate_image_urls(value):
    if not value:
        raise ValueError("Field image_urls is empty.")
    elif not isinstance(value, list):
        raise ValueError("Field image_urls must be list")
    return value


def validate_description(value):
    if not value:
        raise ValueError("Field description is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field description must be str")
    return value


def validate_raw_description(value):
    if not value:
        raise ValueError("Field raw_description is empty.")
    elif not isinstance(value, str):
        raise ValueError("Field raw_description must be str")
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

    product_name_in = MapCompose(validate_product_name)
    product_id_in = MapCompose(validate_product_id)
    link_in = MapCompose(validate_link)
    designer_in = MapCompose(validate_designer)
    color_in = MapCompose(validate_color)
    # price_in = MapCompose(validate_price)
    # sale_price_in = MapCompose(validate_sale_price)
    stock_status_in = MapCompose(validate_stock_status)
    image_urls_in = MapCompose(validate_image_urls)
    description_in = MapCompose(validate_description, escape_html, strip_html)

    product_name_out = Join()

    def add_item_prices(self, product):
        price_data = product["price"]

        price = 0.00
        sale_price = 0.00

        if price_data.get("list"):
            price = price_data["list"]["value"]
            sale_price = price_data["sales"]["value"]
        else:
            price = price_data["sales"]["value"] or price_data["min"]["sales"]["value"]

        self.add_value("price", price)
        self.add_value("sale_price", sale_price)

    def add_item_images(self, product):
        self.add_value("image_urls", [i["absURL"] for i in product["images"]["hi-res"]])
