import html
from abc import ABC, abstractmethod

import html2text
from itemloaders.processors import Compose, Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from brahmin_spider.items import BrahminSpiderItem


def escape_html(html_text: str) -> str:
    """
    Escape HTML entities e.g. replace &gt; with >.

    Args:
        html_text (str): HTML text input.

    Returns:
        str: Return unescaped HTML string.
    """
    return html.unescape(html_text)


def strip_html(html_text: str) -> str:
    """
    Strips html tags out of a string.

    Args:
        html_text (str): HTML text input.

    Returns:
        str: Return text without any html tags.
    """
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text = text_maker.handle(html_text)
    return text


class DataLoader(ABC):
    @abstractmethod
    def add_item_prices(self, product):
        pass

    @abstractmethod
    def add_item_images(self, product):
        pass


class ProductLoader(DataLoader, ItemLoader):
    default_item_class = BrahminSpiderItem  # Specify the item class for this loader
    """
    Input and output processors are used to clean and
    preprocess data within the Scrapy item pipeline.

    Purpose: Input and output processors in Scrapy are used to clean and preprocess
    scraped data as it flows through the Scrapy item pipeline.

    Usage: Input processors are applied to data when it is initially extracted from
    the web page, while output processors are applied before the data is stored or exported.

    Implementation: Processors are implemented as Python functions or methods that you
    define in your Scrapy project. They are applied to specific fields of the scraped items,
    allowing you to clean, validate, or transform the data as needed.
    """

    # Input processors
    description_in = MapCompose(escape_html, strip_html)

    # Output processors
    product_name_out = TakeFirst()
    product_id_out = TakeFirst()
    designer_out = TakeFirst()
    color_out = TakeFirst()
    link_out = TakeFirst()
    price_out = TakeFirst()
    sale_price_out = TakeFirst()
    stock_status_out = TakeFirst()
    description_out = Join()

    def add_item_prices(self, product):
        price_data = product["price"]

        sale_price = float(0.00)

        if price_data.get("list"):
            price = float(price_data["list"]["value"])
            sale_price = float(price_data["sales"]["value"])
        else:
            price = float(price_data["sales"]["value"]) or float(
                price_data["min"]["sales"]["value"]
            )

        self.add_value("price", price)
        self.add_value("sale_price", sale_price)

    def add_item_images(self, product):
        self.add_value("image_urls", [i["absURL"] for i in product["images"]["hi-res"]])
