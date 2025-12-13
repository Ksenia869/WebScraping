# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FilmItem(scrapy.Item):
    title = scrapy.Field()
    release_date = scrapy.Field()
    description = scrapy.Field()
    genres = scrapy.Field()
    country_year = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
