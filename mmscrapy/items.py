# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PageListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kind = Field()
    count = Field()
    urls = Field()
    names = Field()


class ImageListItem(scrapy.Item):
    count = Field()
    father_url = Field()
    urls = Field()
