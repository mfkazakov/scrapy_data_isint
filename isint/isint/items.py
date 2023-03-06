# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional
from scrapy.item import Field


class ItemZakupkiDishonest(scrapy.Item):
    fz = Field()
    number = Field()
    href = Field()
    name = Field()
    inn = Field()
    status = Field()
    add = Field()
    delete = Field()
    update = Field()


class IsintItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ItemHsFromPage(scrapy.Item):
    site = Field()
    response_kod = Field()
    h1 = Field()
    h2 = Field()
    h3 = Field()
    h4 = Field()
