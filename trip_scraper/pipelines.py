import logging
from sqlalchemy.exc import SQLAlchemyError
from trip_scraper.models.hotel import Hotel
from trip_scraper.utils.database import SessionLocal

class TripScraperPipeline:
    def __init__(self):
        self.session = SessionLocal()

    def process_item(self, item, spider):
        try:
            hotel = Hotel(
                title=item['title'],
                rating=float(item['rating']) if item['rating'] else None,
                reviews_count=item['reviews_count'],
                location=', '.join(item['location']) if item['location'] else None,
                room_type=item['room_type'],
                price=item['price'],
                image_urls=','.join(item['image_urls']),
                city=item['city']
            )

            self.session.add(hotel)
            self.session.commit()
            logging.info(f"Successfully added hotel: {item['title']}")
        except SQLAlchemyError as e:
            logging.error(f"Database error: {str(e)}")
            self.session.rollback()
        except Exception as e:
            logging.error(f"Error processing item: {str(e)}")
            self.session.rollback()
        return item

    def close_spider(self, spider):
        self.session.close()