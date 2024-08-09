import scrapy
import json


# class TripSpider(scrapy.Spider):
#     name = "trip_spider"
#     allowed_domains = ["uk.trip.com"]
#     start_urls = [
#         "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"
#     ]

#     custom_settings = {
#         'ROBOTSTXT_OBEY': False,
#     }

#     def parse(self, response):
#         # Make the API request to fetch the hotel data
#         api_url = "https://uk.trip.com/htls/getHotelList?x-traceID=1723089267152.c51bcuXAnVpv-1723177393294-1535315718"
#         yield scrapy.Request(api_url, callback=self.parse_hotel_data)

#     def parse_hotel_data(self, response):
#         # Parse the JSON response
#         data = json.loads(response.text)

#         # Extract hotel information
#         for hotel in data["hotelList"]:
#             hotel_info = hotel["hotelBasicInfo"]
#             hotel_data = {
#                 'hotel_id': hotel_info.get('hotelId'),
#                 'name': hotel_info.get('hotelName'),
#                 'address': hotel_info.get('hotelAddress'),
#                 'price': hotel_info.get('price'),
#                 'origin_price': hotel_info.get('originPrice'),
#                 'rating': hotel.get('commentInfo', {}).get('commentScore'),
#                 'reviews': hotel.get('commentInfo', {}).get('commenterNumber'),
#                 'latitude': hotel.get('positionInfo', {}).get('coordinate', {}).get('lat'),
#                 'longitude': hotel.get('positionInfo', {}).get('coordinate', {}).get('lng'),
#             }

#             yield hotel_data

            
# import scrapy
# import json

# class TripSpider(scrapy.Spider):
#     name = 'trip_spider'
#     allowed_domains = ['uk.trip.com']
#     start_urls = ['https://uk.trip.com/htls/getHotDestination?x-traceID=1723089267152.c51bcuXAnVpv-1723196664486-1246486201']

#     custom_settings = {
#         'ROBOTSTXT_OBEY': False,
#     }

#     def start_requests(self):
#         headers = {
#             'accept': 'application/json',
#             'accept-language': 'en-US,en;q=0.9',
#             'content-type': 'application/json',
#             'cookie': 'your_cookie_here',  # Replace with the actual cookie
#             'currency': 'GBP',
#             'locale': 'en-GB',
#             'origin': 'https://uk.trip.com',
#             'p': '93459017815',
#             'pid': '72a446c9-0fbc-48ab-b298-838f200ade4d',
#             'priority': 'u=1, i',
#             'referer': 'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP',
#             'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Linux"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-origin',
#             'trip-trace-id': '1723089267152.c51bcuXAnVpv-1723196664486-1246486201',
#             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#             'x-traceid': '1723089267152.c51bcuXAnVpv-1723196664486-1246486201'
#         }

#         body = json.dumps({
#             "lastUpdateTime": 0,
#             "newHotDestinationFlag": True,
#             "allDataFlag": True,
#             "head": {
#                 "platform": "PC",
#                 "clientId": "1723089267152.c51bcuXAnVpv",
#                 "bu": "ibu",
#                 "group": "TRIP",
#                 "aid": "",
#                 "sid": "",
#                 "ouid": "",
#                 "caid": "",
#                 "csid": "",
#                 "couid": "",
#                 "region": "GB",
#                 "locale": "en-GB",
#                 "timeZone": "6",
#                 "currency": "GBP",
#                 "p": "93459017815",
#                 "pageID": "10320668150",
#                 "deviceID": "PC",
#                 "clientVersion": "0",
#                 "frontend": {
#                     "vid": "1723089267152.c51bcuXAnVpv",
#                     "sessionID": "8",
#                     "pvid": "19"
#                 },
#                 "extension": [
#                     {"name": "cityId", "value": ""},
#                     {"name": "checkIn", "value": ""},
#                     {"name": "checkOut", "value": ""}
#                 ],
#                 "tripSub1": "",
#                 "qid": "",
#                 "pid": "72a446c9-0fbc-48ab-b298-838f200ade4d",
#                 "hotelExtension": {},
#                 "cid": "1723089267152.c51bcuXAnVpv",
#                 "traceLogID": "e3b75c6d094b8",
#                 "ticket": "",
#                 "href": "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"
#             }
#         })

#         yield scrapy.Request(
#             url=self.start_urls[0],
#             method='POST',
#             headers=headers,
#             body=body,
#             callback=self.parse
#         )

#     def parse(self, response):
#         data = json.loads(response.text)
#         destinations = data.get('group', [])

#         all_destinations = {}
#         for group in destinations:
#             hot_destinations = group.get('hotDestination', [])
#             for destination in hot_destinations:
#                 display_name = destination.get('displayName')
#                 dest_id = destination.get('id')
#                 if display_name and dest_id:
#                     all_destinations[display_name] = dest_id

#         yield {'destinations': all_destinations}


import scrapy
import json
from urllib.parse import urlencode
from datetime import datetime, timedelta

class TripSpider(scrapy.Spider):
    name = 'trip_spider'
    allowed_domains = ['uk.trip.com']
    start_urls = ['https://uk.trip.com/htls/getHotDestination?x-traceID=1723089267152.c51bcuXAnVpv-1723196664486-1246486201']

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, *args, **kwargs):
        super(TripSpider, self).__init__(*args, **kwargs)
        self.destinations_data = {}


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
        estinations_data={}
        data = json.loads(response.text)
        destinations = data.get('group', [])

        checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")
        checkout_date = (datetime.now() + timedelta(days=2)).strftime("%Y/%m/%d")

        for group in destinations:
            hot_destinations = group.get('hotDestination', [])
            for destination in hot_destinations:
                display_name = destination.get('displayName')
                dest_id = destination.get('id')
                if display_name and dest_id:
                    url = f"https://uk.trip.com/hotels/list?city={dest_id}&checkin={checkin_date}&checkout={checkout_date}"
                    self.destinations_data[display_name] = url

        # Yield all destination data at once
        yield self.destinations_data
        print('=========================================================================================')



class HotelSpider(scrapy.Spider):
    name = 'hotel_spider'
    start_urls = ['https://uk.trip.com/hotels/list?city=338&checkin=2024/8/9&checkout=2024/08/10']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        hotels = response.css('div.with-decorator-wrap-v8')

        for hotel in hotels:
            yield {
                'name': hotel.css('span.name::text').get(),
                'rating': hotel.css('div.score .real::text').get(),
                'review_count': hotel.css('div.count a::text').get(),
                'price': hotel.css('div.real span::text').get(),
                'image_url': hotel.css('img.m-lazyImg__img::attr(src)').get(),
                'location': hotel.css('p.transport span.map::text').get()
            }
