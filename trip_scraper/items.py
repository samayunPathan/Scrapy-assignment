import scrapy

class TripScraperItem(scrapy.Item):
    pass

import scrapy

class HotelItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    reviews_count = scrapy.Field()
    location = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
