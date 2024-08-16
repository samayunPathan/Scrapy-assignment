from trip_scraper.models.hotel import Hotel, Session

class TripScraperPipeline:
    def __init__(self):
        self.session = Session()

    def process_item(self, item, spider):
        # Convert the list of images to a comma-separated string
        images_str = ','.join(item['images']) if item['images'] else None

        # Create a new Hotel object
        hotel = Hotel(
            hotelName=item['hotelName'],
            description=item.get('description'),
            lat=item.get('lat'),
            lon=item.get('lon'),
            rating=item.get('rating'),
            amenities=item.get('amenities'),
            images=images_str,
            address=item.get('address'),
            cityName=item.get('cityName')
        )

        # Add the hotel to the session and commit the transaction
        try:
            self.session.add(hotel)
            self.session.commit()
            spider.logger.info(f"Hotel '{hotel.hotelName}' stored in the database.")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Failed to store hotel '{hotel.hotelName}': {str(e)}")

        return item

    def close_spider(self, spider):
        # Close the session when the spider is closed
        self.session.close()

