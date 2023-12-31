# -*- coding: utf-8 -*-
import simplejson
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pyquery import PyQuery
from brahmin_spider.items import BrahminSpiderItem
from brahmin_spider.loaders import ProductLoader


class BrahminSpider(CrawlSpider):
    name = "brahmin"
    allowed_domains = ["brahmin.com"]
    start_urls = ["https://www.brahmin.com/home/"]

    rules = (
        Rule(LinkExtractor(restrict_css=".nav-link")),
        Rule(
            LinkExtractor(restrict_css=".loadmore", tags=["button"], attrs=["data-url"])
        ),
        Rule(
            LinkExtractor(restrict_css=".product-tile"), callback="parse_item_variants"
        ),
    )

    def parse_item_variants(self, response):
        pq = PyQuery(response.body)

        for button in pq(".color-attribute.selectable").items():
            url = button.attr("data-url")
            yield Request(
                url,
                cb_kwargs={"product_name": pq(".product-name").text()},
                callback=self.parse_item,
            )

    def parse_item(self, response, product_name):
        product = simplejson.loads(response.body)["product"]

        loader = ProductLoader(item=BrahminSpiderItem(), response=response)
        # Default loaders
        loader.add_value("product_name", product_name)
        loader.add_value("product_id", product["id"])
        loader.add_value("link", response.urljoin(product["selectedProductUrl"]))
        loader.add_value("designer", "Brahmin")
        loader.add_value("color", product["color"])
        loader.add_value("stock_status", product["available"])
        loader.add_value("description", product["shortDescription"])
        loader.add_value("raw_description", product["shortDescription"])
        # Custom loaders
        loader.add_item_prices(product)
        loader.add_item_images(product)

        item = loader.load_item()
        yield item
