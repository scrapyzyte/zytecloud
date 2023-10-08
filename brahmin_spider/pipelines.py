# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re

import hashlib

# useful for handling different item types with a single interface
from scrapy import Request
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


def is_valid_link(link: str) -> bool:
    """
    Define a regular expression pattern to match URLs with http or https schemes and a domain.

    Args:
        link (str): URL.

    Returns:
        bool: Return true if the link matches the pattern.
    """
    pattern = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}(/.*)?$"
    try:
        if re.match(pattern, str(link)):
            return True
    except ValueError:
        return False
    return False


def is_valid_price(price: float) -> bool:
    """
    Implement your price validation logic here.
    For example, check if the price is a valid number and within a certain range.

    Args:
        price (float): price.

    Returns:
        bool: Return true if price is valid.
    """
    try:
        price = float(price)
        if price < 0:
            return False
    except ValueError:
        return False
    return True


def validate_data_type(item_adapter: any, data_type: type, validate_list: list) -> bool:
    for field in validate_list:
        if not isinstance(item_adapter.get(field), data_type):
            raise DropItem(
                f"Invalid data in '{field}' field. It should be a '{data_type}'."
            )
    return True


class ValidateItemFilterPipeline:
    # required_fields = ['product_id', 'link', 'product_name', "image_urls"]
    required_fields = [
        "product_name",
        "product_id",
        "link",
        "designer",
        "color",
        "price",
        # "sale_price",
        "stock_status",
        "image_urls",
        "description",
    ]

    validate_string = [
        "product_name",
        "product_id",
        "link",
        "designer",
        "color",
        "description",
    ]

    validate_float = [
        "price",
        # "sale_price",
    ]

    validate_list = [
        "image_urls",
    ]

    validate_boolean = [
        "stock_status",
    ]

    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)

        # Validate all fields. Data needs to be populated in all fields listed in required_fields.
        missing_fields = [
            field for field in self.required_fields if not item_adapter.get(field)
        ]
        if missing_fields:
            raise DropItem(f"Missing fields: {', '.join(missing_fields)} ~> {item}")

        # Validate data type.
        validate_data_type(item_adapter, str, self.validate_string)
        validate_data_type(item_adapter, float, self.validate_float)
        validate_data_type(item_adapter, list, self.validate_list)
        validate_data_type(item_adapter, bool, self.validate_boolean)

        # Validate link structure for the link field.
        if not is_valid_link(item_adapter.get("link")):
            raise DropItem(f"Product link is not valid: {item}")

        # Validate link structure for the image_urls field.
        for image_url in item_adapter.get("image_urls"):
            if not is_valid_link(image_url):
                raise DropItem(f"Image link is not valid: {image_url} ~> {item}")

        # Validate price for the price field.
        price = item_adapter.get("price")
        if not is_valid_price(price):
            raise DropItem(f"Invalid price value: {price}")

        return item


class DuplicateItemFilterPipeline:
    def __init__(self):
        self.seen_items = set()

    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)

        product_id = item_adapter.get("product_id")
        product_id = product_id.strip().lower() if product_id else ""

        color = item_adapter.get("color")
        color = color.strip().lower() if color else ""

        item_key = f"{product_id}_{color}"

        if item_key in self.seen_items:
            raise DropItem(f'Duplicate item found: {item_key} ~> {item}')
        self.seen_items.add(item_key)

        return item


class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{item['product_id']}/{item['color']}/full/{image_guid}.jpg"

    def thumb_path(self, request, thumb_id, response=None, info=None, *, item=None):
        thumb_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{item['product_id']}/{item['color']}/thumbs/{thumb_id}/{thumb_guid}.jpg"
