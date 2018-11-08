# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def add_jobbole(value):
    return value + "crh"


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
        # input_processor=MapCompose(add_jobbole)
        input_processor=MapCompose(lambda x: x + 'jobbole', add_jobbole),
        output_processor=TakeFirst()
    )

    create_time = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    vote = scrapy.Field()
    bookmark = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()


class ArticleItem(ItemLoader):
    # 自定义itemloder
    default_output_processor = TakeFirst()
