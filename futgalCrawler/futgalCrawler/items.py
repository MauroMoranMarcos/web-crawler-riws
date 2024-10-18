# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FutgalcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    team = scrapy.Field()
    pass

class MatchItem(scrapy.Item):
    home_team = scrapy.Field()
    away_team = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    field = scrapy.Field()
    referee = scrapy.Field()
    pass
