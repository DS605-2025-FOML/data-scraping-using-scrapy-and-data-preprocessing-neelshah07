# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class book(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    product_page = scrapy.Field()  # URL of the book detail page
