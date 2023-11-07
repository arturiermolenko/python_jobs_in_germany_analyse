# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArbeitsAgenturScrapeItem(scrapy.Item):
    position = scrapy.Field()
    profession = scrapy.Field()
    city = scrapy.Field()
    company_name = scrapy.Field()
    description = scrapy.Field()
