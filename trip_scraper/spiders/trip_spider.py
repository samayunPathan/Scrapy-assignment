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
        script_text = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        if not script_text:
            self.logger.error("Script tag not found or empty.")
            return

        try:
            json_str = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)
            json_data = json.loads(json_str).get('initData', {}).get('htlsData', {})
        except (AttributeError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to extract JSON data. Error: {str(e)}")
            return

        categories = [
            ('fiveStarHotels', 'fiveStarHotels'),
            ('cheapHotels', 'cheapHotels'),
            ('hostelHotels', 'hostelHotels'),
            ('inboundCities', 'inboundCities'),
            ('outboundCities', 'outboundCities')
        ]

        try:
            selected_categories = random.sample(categories, min(3, len(categories)))
        except ValueError as e:
            self.logger.error(f"Error sampling categories: {str(e)}")
            selected_categories = categories

        for category_name, json_key in selected_categories:
            if category_name in ['inboundCities', 'outboundCities']:
                city = next(iter(json_data.get(json_key, [])), None)
                if city:
                    city_id = city.get('id')
                    hotel = next(iter(city.get('recommendHotels', [])), None)
                    if hotel:
                        hotel_data = self.extract_hotel_data(hotel)
                        hotel_data['city_id'] = city_id
                        yield hotel_data
            else:
                for hotel in json_data.get(json_key, []):
                    yield self.extract_hotel_data(hotel)

    def extract_hotel_data(self, hotel):
        images = [hotel.get('imgUrl')] if hotel.get('imgUrl') else []
        images.extend([pic['pictureUrl'] for pic in hotel.get('pictureList', [])[:1] if 'pictureUrl' in pic])
        relative_image_paths = self.save_images(images, hotel.get('hotelName'))
        
        amenities = ",".join(facility.get('name', '') for facility in hotel.get('hotelFacilityList', []))

        return HotelItem(
            hotelId=hotel.get('hotelId'),
            hotelName=hotel.get('hotelName'),
            description=hotel.get('brief'),
            lat=hotel.get('lat'),
            lon=hotel.get('lon'),
            rating=hotel.get('rating'),
            amenities=amenities,
            images=relative_image_paths,
            address=hotel.get('address'),
            cityName=hotel.get('cityName'),
            city_id=hotel.get('city_id')
        )

    def save_images(self, images, hotel_name):
        safe_hotel_name = re.sub(r'[^a-zA-Z0-9]', '_', hotel_name)
        directory = os.path.join('images', safe_hotel_name)
        os.makedirs(directory, exist_ok=True)

        relative_paths = []
        for i, url in enumerate(images):
            url = url.lstrip("/")
            full_url = urllib.parse.urljoin('https://ak-d.tripcdn.com/images/', url)
            image_path = os.path.join(directory, f'image_{i + 1}.jpg')
            try:
                urllib.request.urlretrieve(full_url, image_path)
                self.logger.info(f"Saved image {i + 1} for hotel '{hotel_name}' at {image_path}")
                relative_paths.append(os.path.relpath(image_path, start='images'))
            except Exception as e:
                self.logger.error(f"Failed to save image {i + 1} for hotel '{hotel_name}' from URL {full_url}: {str(e)}")

        return relative_paths
