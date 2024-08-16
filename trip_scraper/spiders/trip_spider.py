# import scrapy
# import json
# import re
# from scrapy.http import HtmlResponse
# from trip_scraper.items import HotelItem


# class TripSpider(scrapy.Spider):
#     name = "trip_spider"
#     allowed_domains = ["trip.com"]
#     start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

#     custom_settings = {
#         'ROBOTSTXT_OBEY': False
#     }

#     def parse(self, response: HtmlResponse):
#         # Extract the script tag containing the desired data
#         script_text = response.xpath(
#             '//script[contains(text(), "window.IBU_HOTEL")]/text()'
#         ).get()

#         if script_text:
#             try:
#                 # Extract the JSON part of the script using regular expression
#                 json_str = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)
#                 json_data = json.loads(json_str).get('initData', {}).get('htlsData', {})

#                 # Extract and yield data for five-star hotels
#                 for hotel in json_data.get('fiveStarHotels', []):
#                     yield self.extract_hotel_data(hotel)

#                 # Extract and yield data for cheap hotels
#                 for hotel in json_data.get('chepHotels', []):
#                     yield self.extract_hotel_data(hotel)

#                 # Extract and yield data for hostel hotels
#                 for hotel in json_data.get('hostelHotels', []):
#                     yield self.extract_hotel_data(hotel)

#                 # Extract and yield data for inbound cities
#                 for city in json_data.get('inboundCites', []):
#                     for hotel in city.get('recommendHotels', []):
#                         yield self.extract_hotel_data(hotel)

#                 # Extract and yield data for outbound cities
#                 for city in json_data.get('outboundCities', []):
#                     for hotel in city.get('recommendHotels', []):
#                         yield self.extract_hotel_data(hotel)

#             except (AttributeError, json.JSONDecodeError) as e:
#                 self.logger.error(f"Failed to extract JSON data. Error: {str(e)}")
#         else:
#             self.logger.error("Script tag not found or empty.")

#     def extract_hotel_data(self, hotel):
#         """Extract relevant hotel data from the JSON object."""
#         # Start with imgUrl if available
#         images = [hotel.get('imgUrl')] if hotel.get('imgUrl') else []

#         # Extend with URLs from pictureList where each entry is a dictionary with 'pictureUrl'
#         images.extend([pic['pictureUrl'] for pic in hotel.get('pictureList', []) if 'pictureUrl' in pic])

#         return HotelItem (
#             hotelName= hotel.get('hotelName'),
#             description=hotel.get('brief'),
#             lat= hotel.get('lat'),
#             lon= hotel.get('lon'),
#             rating= hotel.get('rating'),
#             images= images,  # Combined list of all image URLs
#             address= hotel.get('address'),
#             cityName= hotel.get('cityName')
#         )


import scrapy
import json
import re
import os
import urllib.request
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
        """Extract relevant hotel data from the JSON object and save images."""
        # Start with imgUrl if available
        images = [hotel.get('imgUrl')] if hotel.get('imgUrl') else []

        # Extend with URLs from pictureList where each entry is a dictionary with 'pictureUrl'
        images.extend([pic['pictureUrl'] for pic in hotel.get('pictureList', []) if 'pictureUrl' in pic])

        # Log the extracted image URLs for debugging
        self.logger.info(f"Extracted image URLs for hotel '{hotel.get('hotelName')}': {images}")

        # Download the images
        self.save_images(images, hotel.get('hotelName'))

        return HotelItem(
            hotelName=hotel.get('hotelName'),
            description=hotel.get('brief'),
            lat=hotel.get('lat'),
            lon=hotel.get('lon'),
            rating=hotel.get('rating'),
            images=images,  # Combined list of all image URLs
            address=hotel.get('address'),
            cityName=hotel.get('cityName')
        )

    def save_images(self, images, hotel_name):
        """Save images to a local directory."""
        # Ensure hotel name is valid for folder creation
        safe_hotel_name = re.sub(r'[^a-zA-Z0-9]', '_', hotel_name)
        directory = os.path.join('images', safe_hotel_name)

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        for i, url in enumerate(images):
            # Ensure that the URL doesn't start with a slash before joining
            if url.startswith("/"):
                url = url.lstrip("/")  # Remove the leading slash

            # Construct the full image URL
            full_url = urllib.parse.urljoin('https://ak-d.tripcdn.com/images/', url)
            
            image_path = os.path.join(directory, f'image_{i + 1}.jpg')
            try:
                # Log the full URL being downloaded for debugging
                self.logger.info(f"Downloading image from URL: {full_url}")

                urllib.request.urlretrieve(full_url, image_path)
                self.logger.info(f"Saved image {i + 1} for hotel '{hotel_name}' at {image_path}")
            except Exception as e:
                self.logger.error(f"Failed to save image {i + 1} for hotel '{hotel_name}' from URL {full_url}: {str(e)}")
