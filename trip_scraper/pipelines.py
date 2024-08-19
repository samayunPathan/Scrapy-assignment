# from trip_scraper.models.hotel import Hotel, Session

# class TripScraperPipeline:
#     def __init__(self):
#         self.session = Session()

#     def process_item(self, item, spider):
#         # Convert the list of relative image paths to a comma-separated string
#         images_str = ','.join(item['images']) if item['images'] else None

#         # Try to find an existing hotel by hotelId
#         hotel = self.session.query(Hotel).filter_by(hotelId=item['hotelId']).first()

#         if hotel:
#             # Update existing hotel
#             hotel.hotelName = item['hotelName']
#             hotel.description = item.get('description')
#             hotel.lat = item.get('lat')
#             hotel.lon = item.get('lon')
#             hotel.rating = item.get('rating')
#             hotel.amenities = item.get('amenities')
#             hotel.images = images_str  # Store the relative image paths
#             hotel.address = item.get('address')
#             hotel.cityName = item.get('cityName')
#         else:
#             # Create a new hotel
#             hotel = Hotel(
#                 hotelId=item['hotelId'],
#                 hotelName=item['hotelName'],
#                 description=item.get('description'),
#                 lat=item.get('lat'),
#                 lon=item.get('lon'),
#                 rating=item.get('rating'),
#                 amenities=item.get('amenities'),
#                 images=images_str,  # Store the relative image paths
#                 address=item.get('address'),
#                 cityName=item.get('cityName')
#             )
#             self.session.add(hotel)

#         # Commit the transaction
#         try:
#             self.session.commit()
#             spider.logger.info(f"Hotel '{hotel.hotelName}' stored/updated in the database.")
#         except Exception as e:
#             self.session.rollback()
#             spider.logger.error(f"Failed to store/update hotel '{hotel.hotelName}': {str(e)}")

#         return item

#     def close_spider(self, spider):
#         # Close the session when the spider is closed
#         self.session.close()


from trip_scraper.models.hotel import Hotel, Session

class TripScraperPipeline:
    def __init__(self):
        self.session = Session()

    def process_item(self, item, spider):
        # Convert the list of relative image paths to a comma-separated string
        images_str = ','.join(item['images']) if item['images'] else None

        # Try to find an existing hotel by hotelId
        hotel = self.session.query(Hotel).filter_by(hotelId=item['hotelId']).first()

        if hotel:
            # Update existing hotel
            hotel.hotelName = item['hotelName']
            hotel.description = item.get('description')
            hotel.lat = item.get('lat')
            hotel.lon = item.get('lon')
            hotel.rating = item.get('rating')
            hotel.amenities = item.get('amenities')
            hotel.images = images_str  # Store the relative image paths
            hotel.address = item.get('address')
            hotel.cityName = item.get('cityName')
        else:
            # Create a new hotel
            hotel = Hotel(
                hotelId=item['hotelId'],
                hotelName=item['hotelName'],
                description=item.get('description'),
                lat=item.get('lat'),
                lon=item.get('lon'),
                rating=item.get('rating'),
                amenities=item.get('amenities'),
                images=images_str,  # Store the relative image paths
                address=item.get('address'),
                cityName=item.get('cityName')
            )
            self.session.add(hotel)

        # Commit the transaction
        try:
            self.session.commit()
            spider.logger.info(f"Hotel '{hotel.hotelName}' stored/updated in the database.")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Failed to store/update hotel '{hotel.hotelName}': {str(e)}")

        return item

    def close_spider(self, spider):
        # Close the session when the spider is closed
        self.session.close()
