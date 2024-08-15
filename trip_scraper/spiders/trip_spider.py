import scrapy
import json
import re
from scrapy.http import HtmlResponse
from trip_scraper.items import HotelItem


class TripSpider(scrapy.Spider):
    name = "trip_spider"
    allowed_domains = ["trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def parse(self, response: HtmlResponse):
        # Extract the script tag containing the desired data
        script_text = response.xpath(
            '//script[contains(text(), "window.IBU_HOTEL")]/text()'
        ).get()

        if script_text:
            try:
                # Extract the JSON part of the script using regular expression
                json_str = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)
                json_data = json.loads(json_str).get('initData', {}).get('htlsData', {})

                # Extract and yield data for five-star hotels
                for hotel in json_data.get('fiveStarHotels', []):
                    yield self.extract_hotel_data(hotel)

                # Extract and yield data for cheap hotels
                for hotel in json_data.get('chepHotels', []):
                    yield self.extract_hotel_data(hotel)

                # Extract and yield data for hostel hotels
                for hotel in json_data.get('hostelHotels', []):
                    yield self.extract_hotel_data(hotel)

                # Extract and yield data for inbound cities
                for city in json_data.get('inboundCites', []):
                    for hotel in city.get('recommendHotels', []):
                        yield self.extract_hotel_data(hotel)

                # Extract and yield data for outbound cities
                for city in json_data.get('outboundCities', []):
                    for hotel in city.get('recommendHotels', []):
                        yield self.extract_hotel_data(hotel)

            except (AttributeError, json.JSONDecodeError) as e:
                self.logger.error(f"Failed to extract JSON data. Error: {str(e)}")
        else:
            self.logger.error("Script tag not found or empty.")

    def extract_hotel_data(self, hotel):
        """Extract relevant hotel data from the JSON object."""
        # Start with imgUrl if available
        images = [hotel.get('imgUrl')] if hotel.get('imgUrl') else []

        # Extend with URLs from pictureList where each entry is a dictionary with 'pictureUrl'
        images.extend([pic['pictureUrl'] for pic in hotel.get('pictureList', []) if 'pictureUrl' in pic])

        return HotelItem (
            hotelName= hotel.get('hotelName'),
            description=hotel.get('brief'),
            lat= hotel.get('lat'),
            lon= hotel.get('lon'),
            rating= hotel.get('rating'),
            images= images,  # Combined list of all image URLs
            address= hotel.get('address'),
            cityName= hotel.get('cityName')
        )
