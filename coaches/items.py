# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoachesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    position = scrapy.Field()
    link = scrapy.Field()
    team = scrapy.Field()
    year = scrapy.Field()
    win = scrapy.Field()
    loss = scrapy.Field()
    tie = scrapy.Field()