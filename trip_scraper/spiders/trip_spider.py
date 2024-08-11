# # ====== dynamic ======
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="your_app_name")
location = geolocator.geocode("Marina Bay,Singapore")
print((location.latitude, location.longitude))


# # ======   database okay  =======

import scrapy
import json
import os
import random
from urllib.parse import urljoin
from datetime import datetime, timedelta
from trip_scraper.utils.database import init_db


class TripSpider(scrapy.Spider):
    name = 'trip_spider'
    allowed_domains = ['uk.trip.com', 'ak-d.tripcdn.com']
    start_urls = [
        'https://uk.trip.com/htls/getHotDestination?x-traceID=1723089267152.c51bcuXAnVpv-1723196664486-1246486201'
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'OFFSITE_ENABLED': False,
        'ITEM_PIPELINES': {
            'trip_scraper.pipelines.TripScraperPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destinations_data = {}
        self.checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")
        self.checkout_date = (datetime.now() + timedelta(days=2)).strftime("%Y/%m/%d")
        self.urls = []

        # Initialize the database
        init_db()

    def start_requests(self):
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': 'your_cookie_here',  # Replace with the actual cookie
            'currency': 'GBP',
            'locale': 'en-GB',
            'origin': 'https://uk.trip.com',
            'p': '93459017815',
            'pid': '72a446c9-0fbc-48ab-b298-838f200ade4d',
            'priority': 'u=1, i',
            'referer': 'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'trip-trace-id': '1723089267152.c51bcuXAnVpv-1723196664486-1246486201',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-traceid': '1723089267152.c51bcuXAnVpv-1723196664486-1246486201'
        }

        body = json.dumps({
            "lastUpdateTime": 0,
            "newHotDestinationFlag": True,
            "allDataFlag": True,
            "head": {
                "platform": "PC",
                "clientId": "1723089267152.c51bcuXAnVpv",
                "bu": "ibu",
                "group": "TRIP",
                "aid": "",
                "sid": "",
                "ouid": "",
                "caid": "",
                "csid": "",
                "couid": "",
                "region": "GB",
                "locale": "en-GB",
                "timeZone": "6",
                "currency": "GBP",
                "p": "93459017815",
                "pageID": "10320668150",
                "deviceID": "PC",
                "clientVersion": "0",
                "frontend": {
                    "vid": "1723089267152.c51bcuXAnVpv",
                    "sessionID": "8",
                    "pvid": "19"
                },
                "extension": [
                    {"name": "cityId", "value": ""},
                    {"name": "checkIn", "value": ""},
                    {"name": "checkOut", "value": ""}
                ],
                "tripSub1": "",
                "qid": "",
                "pid": "72a446c9-0fbc-48ab-b298-838f200ade4d",
                "hotelExtension": {},
                "cid": "1723089267152.c51bcuXAnVpv",
                "traceLogID": "e3b75c6d094b8",
                "ticket": "",
                "href": "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"
            }
        })

        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            headers=headers,
            body=body,
            callback=self.parse_destinations
        )

    def parse_destinations(self, response):
        data = json.loads(response.text)
        destinations = data.get('group', [])

        self.urls = []
        for group in destinations:
            hot_destinations = group.get('hotDestination', [])
            for destination in hot_destinations:
                display_name = destination.get('displayName')
                dest_id = destination.get('id')
                if display_name and dest_id:
                    url = f"https://uk.trip.com/hotels/list?city={dest_id}&checkin={self.checkin_date}&checkout={self.checkout_date}"
                    self.urls.append((display_name, url))

        # If you have URLs, choose a random one and prompt the user
        if self.urls:
            self.log('Available destinations:')
            for idx, (name, _) in enumerate(self.urls):
                self.log(f'{idx + 1}: {name}')

            # This is a placeholder for user input; in real application, it should be handled through user interface or command line.
            user_choice = random.randint(0, len(self.urls) - 1)  # Example: random choice for demonstration
            chosen_url = self.urls[user_choice][1]
            yield scrapy.Request(chosen_url, callback=self.parse_hotels, meta={'city': self.urls[user_choice][0]})

    def parse_hotels(self, response):
        city = response.meta['city']
        hotels = response.css('div.with-decorator-wrap-v8')

        for hotel in hotels:
            title = hotel.css('.list-card-title .name::text').get()
            rating = hotel.css('.score .real::text').get()
            reviews_count = hotel.css('.count a::text').get()
            location = hotel.css('.list-card-transport-v8 .transport span::text').getall()[:2]
            room_type = hotel.css('.room-type .room-panel-roominfo-name::text').get()
            price = hotel.css('.whole .real.labelColor div::text').get()
            image_urls = hotel.css('.multi-images .m-lazyImg.multi-images-item .m-lazyImg__img::attr(src)').getall()

            yield {
                'title': title,
                'rating': rating,
                'reviews_count': reviews_count,
                'location': location,
                'room_type': room_type,
                'price': price,
                'image_urls': image_urls,
                'city': city,
            }

            image_urls = hotel.css('.multi-images .m-lazyImg.multi-images-item .m-lazyImg__img::attr(src)').getall()
            for idx, image_url in enumerate(image_urls):
                image_url = urljoin(response.url, image_url)
                yield scrapy.Request(image_url, callback=self.save_image, meta={'idx': idx, 'title': title})

    def save_image(self, response):
        directory = f'images/{response.meta["title"].replace(" ", "_")}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        idx = response.meta['idx']
        image_path = os.path.join(directory, f'image_{idx}.jpg')
        with open(image_path, 'wb') as file:
            file.write(response.body)

        self.log(f'Saved image {image_path}')



# ===== ********* for latitude,longitude ******** ===========

from geopy.geocoders import Nominatim
from scrapy import Spider
import json
import os
import random
from urllib.parse import urljoin
from datetime import datetime, timedelta
from trip_scraper.utils.database import init_db

class TripSpiderL(Spider):
    name = 'trip_spiderL'
    allowed_domains = ['uk.trip.com', 'ak-d.tripcdn.com']
    start_urls = [
        'https://uk.trip.com/htls/getHotDestination?x-traceID=1723089267152.c51bcuXAnVpv-1723196664486-1246486201'
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'OFFSITE_ENABLED': False,
        'ITEM_PIPELINES': {
            'trip_scraper.pipelines.TripScraperPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destinations_data = {}
        self.checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")
        self.checkout_date = (datetime.now() + timedelta(days=2)).strftime("%Y/%m/%d")
        self.urls = []

        # Initialize the database
        init_db()

        # Initialize the geolocator
        self.geolocator = Nominatim(user_agent="your_app_name")

    def start_requests(self):
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': 'your_cookie_here',  # Replace with the actual cookie
            'currency': 'GBP',
            'locale': 'en-GB',
            'origin': 'https://uk.trip.com',
            'p': '93459017815',
            'pid': '72a446c9-0fbc-48ab-b298-838f200ade4d',
            'priority': 'u=1, i',
            'referer': 'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'trip-trace-id': '1723089267152.c51bcuXAnVpv-1723196664486-1246486201',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-traceid': '1723089267152.c51bcuXAnVpv-1723196664486-1246486201'
        }

        body = json.dumps({
            "lastUpdateTime": 0,
            "newHotDestinationFlag": True,
            "allDataFlag": True,
            "head": {
                "platform": "PC",
                "clientId": "1723089267152.c51bcuXAnVpv",
                "bu": "ibu",
                "group": "TRIP",
                "aid": "",
                "sid": "",
                "ouid": "",
                "caid": "",
                "csid": "",
                "couid": "",
                "region": "GB",
                "locale": "en-GB",
                "timeZone": "6",
                "currency": "GBP",
                "p": "93459017815",
                "pageID": "10320668150",
                "deviceID": "PC",
                "clientVersion": "0",
                "frontend": {
                    "vid": "1723089267152.c51bcuXAnVpv",
                    "sessionID": "8",
                    "pvid": "19"
                },
                "extension": [
                    {"name": "cityId", "value": ""},
                    {"name": "checkIn", "value": ""},
                    {"name": "checkOut", "value": ""}
                ],
                "tripSub1": "",
                "qid": "",
                "pid": "72a446c9-0fbc-48ab-b298-838f200ade4d",
                "hotelExtension": {},
                "cid": "1723089267152.c51bcuXAnVpv",
                "traceLogID": "e3b75c6d094b8",
                "ticket": "",
                "href": "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"
            }
        })

        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            headers=headers,
            body=body,
            callback=self.parse_destinations
        )

    def parse_destinations(self, response):
        data = json.loads(response.text)
        destinations = data.get('group', [])

        self.urls = []
        for group in destinations:
            hot_destinations = group.get('hotDestination', [])
            for destination in hot_destinations:
                display_name = destination.get('displayName')
                dest_id = destination.get('id')
                if display_name and dest_id:
                    url = f"https://uk.trip.com/hotels/list?city={dest_id}&checkin={self.checkin_date}&checkout={self.checkout_date}"
                    self.urls.append((display_name, url))

        if self.urls:
            self.log('Available destinations:')
            for idx, (name, _) in enumerate(self.urls):
                self.log(f'{idx + 1}: {name}')

            user_choice = random.randint(0, len(self.urls) - 1)  # Example: random choice for demonstration
            chosen_url = self.urls[user_choice][1]
            yield scrapy.Request(chosen_url, callback=self.parse_hotels, meta={'city': self.urls[user_choice][0]})
    
    def parse_hotels(self, response):
        city = response.meta['city']
        hotels = response.css('div.with-decorator-wrap-v8')

        for hotel in hotels:
            title = hotel.css('.list-card-title .name::text').get()
            rating = hotel.css('.score .real::text').get()
            reviews_count = hotel.css('.count a::text').get()
            location = hotel.css('.list-card-transport-v8 .transport span::text').getall()[:-1]
            room_type = hotel.css('.room-type .room-panel-roominfo-name::text').get()
            price = hotel.css('.whole .real.labelColor div::text').get()
            image_urls = hotel.css('div.multi-images div.m-lazyImg.multi-images-item .m-lazyImg__img::attr(src)').getall()

            # Geocoding the hotel location
            full_location = f"{''.join(location[-1])}, {city}"
            loc = self.geolocator.geocode(full_location)
            latitude = loc.latitude if loc else None
            longitude = loc.longitude if loc else None

            # Yield the hotel data including latitude and longitude
            yield {
                'title': title,
                'rating': rating,
                'reviews_count': reviews_count,
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'room_type': room_type,
                'price': price,
                'image_urls': image_urls,
                'city': city,
            }
            image_urls = hotel.css('.multi-images .m-lazyImg.multi-images-item .m-lazyImg__img::attr(src)').getall()
            for idx, image_url in enumerate(image_urls):
                image_url = urljoin(response.url, image_url)
                yield scrapy.Request(image_url, callback=self.save_image, meta={'idx': idx, 'title': title})

    def save_image(self, response):
        directory = f'images/{response.meta["title"].replace(" ", "_")}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        idx = response.meta['idx']
        image_path = os.path.join(directory, f'image_{idx}.jpg')
        with open(image_path, 'wb') as file:
            file.write(response.body)

        self.log(f'Saved image {image_path}')










# # -----  hotel url with header-- -----

# import scrapy
# import json

# class TripSpiderH(scrapy.Spider):
#     name = "tripH"
#     allowed_domains = ['uk.trip.com']
#     start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

#     custom_settings = {
#         'ROBOTSTXT_OBEY': False,
#         'DOWNLOAD_DELAY': 1,
#         'AUTOTHROTTLE_ENABLED': True,
#     }

#     def parse(self, response):
#         script_content = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
#         if script_content:
#             try:
#                 match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_content, re.DOTALL)
#                 if match:
#                     json_str = match.group(1)
#                     data = json.loads(json_str)
                    
#                     # Call the parse_hotel_data method to process the data
#                     results = {}
#                     seo_footer = data.get("initData", {}).get("seoFooter", [])
#                     for entry in seo_footer:
#                         title = entry.get("title")
#                         seo_list = entry.get("seoList", [])
#                         if title and seo_list:
#                             results[title] = {item['name']: item['url'] for item in seo_list}

#                     # Save the data to a JSON file
#                     with open('trip_datav2.json', 'w', encoding='utf-8') as f:
#                         json.dump(results, f, indent=4, ensure_ascii=False)

#                     self.log("Saved file trip_data.json")
#                 else:
#                     self.log("Could not find JSON data in the script", level=scrapy.log.ERROR)
#             except json.JSONDecodeError as e:
#                 self.log(f"Error decoding JSON: {e}", level=scrapy.log.ERROR)
#                 self.log(f"Raw script content: {script_content}", level=scrapy.log.ERROR)
#         else:
#             self.log("No script containing window.IBU_HOTEL found", level=scrapy.log.ERROR)

#     def parse_hotel_data(self, data):
#         # Example: Extracting specific information from the data
#         results = {}
#         seo_footer = data.get("initData", {}).get("seoFooter", [])
#         for entry in seo_footer:
#             title = entry.get("title")
#             seo_list = entry.get("seoList", [])
#             if title and seo_list:
#                 results[title] = {item['name']: item['url'] for item in seo_list}
#         return results











