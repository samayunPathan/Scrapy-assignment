import requests

url = 'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP'
response = requests.get(url)

# Save the response content to a file
with open('page_source.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

print("Page source saved as 'page_source.html'")
