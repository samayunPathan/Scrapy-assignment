import scrapy
import json
import re
import os
import urllib.request
import random
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
                json_str = re.search(
                    r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL
                ).group(1)
                json_data = json.loads(json_str).get('initData', {}).get('htlsData', {})

                # Categories to choose from
                categories = [
                    ('fiveStarHotels', 'fiveStarHotels'),
                    ('chepHotels', 'chepHotels'),
                    ('hostelHotels', 'hostelHotels'),
                    ('inboundCites', 'inboundCites'),
                    ('outboundCities', 'outboundCities')
                ]

                # Randomly select 3 categories
                selected_categories = random.sample(categories, 3)

                # Extract and yield data for the selected categories
                for category_name, json_key in selected_categories:
                    if category_name in ['inboundCites', 'outboundCities']:
                        for city in json_data.get(json_key, []):
                            for hotel in city.get('recommendHotels', []):
                                yield self.extract_hotel_data(hotel)
                    else:
                        for hotel in json_data.get(json_key, []):
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
        images.extend([pic['pictureUrl'] for pic in hotel.get('pictureList', []) if 'pictureUrl' in pic][:1])

        # Log the extracted image URLs for debugging
        self.logger.info(f"Extracted image URLs for hotel '{hotel.get('hotelName')}': {images}")

        # Download the images
        self.save_images(images, hotel.get('hotelName'))
        amenities = [facility.get('name') for facility in hotel.get('hotelFacilityList', [])]
        amenities_str = ",".join(amenities)  # Convert list to comma-separated string

        return HotelItem(
            hotelId =hotel.get('hotelId'),
            hotelName=hotel.get('hotelName'),
            description=hotel.get('brief'),
            lat=hotel.get('lat'),
            lon=hotel.get('lon'),
            rating=hotel.get('rating'),
            amenities=amenities_str,  # Store the amenities string
            images=images,
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
