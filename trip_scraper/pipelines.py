from sqlalchemy.orm import sessionmaker
# from trip_scraper.models import Hotel, engine  # Import both Hotel and engine
from trip_scraper.items import HotelItem

class TripScraperPipeline:
    def __init__(self):
        pass
        # self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if isinstance(item, HotelItem):
            session = self.Session()
            hotel_instance = Hotel(  # Rename to avoid conflict with the class name
                hotelName=item['hotelName'],
                description=item['description'],
                lat=item['lat'],
                lon=item['lon'],
                rating=item['rating'],
                images=item['images'],
                address=item['address'],
                cityName=item['cityName']
            )
            try:
                session.add(hotel_instance)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return item