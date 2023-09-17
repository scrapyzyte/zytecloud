import html
import html2text
from scrapy.loader import ItemLoader
from brahmin_spider.items import BrahminSpiderItem
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose


def escape_html(text):
    """Escape HTML entities e.g. replace &gt; with >"""
    return html.unescape(text)


def strip_html(html_text):
    """Strips html tags out of a string."""
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text = text_maker.handle(html_text)
    return text


class ProductLoader(ItemLoader):
    default_item_class = BrahminSpiderItem  # Specify the item class for this loader

    description_in = MapCompose(escape_html, strip_html)

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
