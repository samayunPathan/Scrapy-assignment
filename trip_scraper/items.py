import scrapy

class TripScraperItem(scrapy.Item):
    pass

class HotelItem(scrapy.Item):
    hotelName = scrapy.Field()
    description = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    rating = scrapy.Field()
    images = scrapy.Field()
    address = scrapy.Field()
    cityName = scrapy.Field()