# import scrapy
# import json

# class TripSpider(scrapy.Spider):
#     name = "trip_spider"
#     allowed_domains = ["uk.trip.com"]
#     start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

#     custom_settings = {
#         'ROBOTSTXT_OBEY': False,
#     }

#     def parse(self, response):
#         # Make the AJAX request to fetch the hotel data
#         ajax_url = "https://m.trip.com/hotels/list/ajax?city=338&checkin=2024/8/2&checkout=2024/08/03"
#         yield scrapy.Request(ajax_url, callback=self.parse_hotel_data)

#     def parse_hotel_data(self, response):
#         # Parse the JSON response
#         data = json.loads(response.text)

#         # Extract the section titles and city names
#         results = []
#         for section in data["data"]["hotelList"]:
#             section_title = section["boundTitle"]
#             city_names = [city["name"] for city in section["boundCities"]]

#             # Store the title and its cities in a dictionary
#             section_data = {
#                 'section_title': section_title,
#                 'cities': city_names
#             }

#             # Add the dictionary to the results list
#             results.append(section_data)

#         # Yield all the results
#         for result in results:
#             yield result

import scrapy
import json

class TripSpider(scrapy.Spider):
    name = "trip_spider"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        # Make the AJAX request to fetch the hotel data
        ajax_url = "https://m.trip.com/hotels/list/ajax?city=338&checkin=2024/8/2&checkout=2024/08/03"
        yield scrapy.Request(ajax_url, callback=self.parse_hotel_data)

    def parse_hotel_data(self, response):
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract the section titles and city names
        results = []
        for section in data["data"]["hotelList"]:
            section_title = section["boundTitle"]
            city_names = [city["name"] for city in section["boundCities"]]

            # Store the title and its cities in a dictionary
            section_data = {
                'section_title': section_title,
                'cities': city_names
            }

            # Add the dictionary to the results list
            results.append(section_data)

        # Yield all the results
        for result in results:
            yield result
