# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ClothesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = Field()
    creationTime = Field()
    id = Field()
    productColor=Field()
    productSize=Field()
    score = Field()
    userClientShow=Field()
    userLevelName = Field()
