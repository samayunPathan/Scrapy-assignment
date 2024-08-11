# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# from trip_scraper.models.hotel import Hotel
# # from trip_scraper.utils.database import get_db_session

# class TripScraperPipeline:
#     # def open_spider(self, spider):
#     #     self.session = get_db_session()

#     # def close_spider(self, spider):
#     #     self.session.close()

#     def process_item(self, item, spider):
#         item = self.clean_data(item)

#         hotel = Hotel(
#             title=item.get('title'),
#             rating=item.get('rating'),
#             reviews_count=item.get('reviews_count'),
#             location=item.get('location'),
#             room_type=item.get('room_type'),
#             price=item.get('price'),
#             image_urls=item.get('image_urls')
#         )

#         # try:
#         #     self.session.add(hotel)
#         #     self.session.commit()
#         # except Exception as e:
#         #     self.session.rollback()
#         #     spider.logger.error(f"Error saving item: {e}")
        
#         return item

#     def clean_data(self, item):
#         """Perform any data cleaning here."""
#         item['title'] = item.get('title', '').strip()
#         item['rating'] = item.get('rating', '').strip()
#         item['reviews_count'] = item.get('reviews_count', '').strip()
#         item['location'] = [loc.strip() for loc in item.get('location', [])]
#         item['room_type'] = item.get('room_type', '').strip()
#         item['price'] = item.get('price', '').strip()
#         item['image_urls'] = [url.strip() for url in item.get('image_urls', [])]
#         return item



# trip_scraper/pipelines.py

# trip_scraper/pipelines.py

# trip_scraper/pipelines.py

# At the top of trip_scraper/pipelines.py
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