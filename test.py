# import requests

# url = 'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP'
# response = requests.get(url)

# # Save the response content to a file
# with open('page_source.html', 'w', encoding='utf-8') as file:
#     file.write(response.text)

# print("Page source saved as 'page_source.html'")

# <div class="transport">
# <div class="real labelColor">
# <span><div>124</div>
# </div>
# </div>

# <div class="transport">
# <span>hello</span>
# <span>world</span>
# <span>hi</span>
# </div>

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
print((location.latitude, location.longitude))
