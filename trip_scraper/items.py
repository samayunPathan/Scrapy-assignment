import scrapy

class HotelItem(scrapy.Item):
    hotelId =scrapy.Field()
    hotelName = scrapy.Field()
    description = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    rating = scrapy.Field()
    amenities = scrapy.Field()  # Corrected field name
    images = scrapy.Field()
    address = scrapy.Field()
    cityName = scrapy.Field()
    city_id = scrapy.Field()  # Add this line



