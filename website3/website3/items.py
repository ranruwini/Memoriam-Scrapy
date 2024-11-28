import scrapy

class QuoteItem(scrapy.Item):
    date = scrapy.Field()
    note = scrapy.Field()
