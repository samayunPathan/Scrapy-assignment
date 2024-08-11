# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from trip_scraper.models.hotel import Hotel
# from trip_scraper.utils.database import get_db_session

class TripScraperPipeline:
    # def open_spider(self, spider):
    #     self.session = get_db_session()

    # def close_spider(self, spider):
    #     self.session.close()

    def process_item(self, item, spider):
        item = self.clean_data(item)

        hotel = Hotel(
            title=item.get('title'),
            rating=item.get('rating'),
            reviews_count=item.get('reviews_count'),
            location=item.get('location'),
            room_type=item.get('room_type'),
            price=item.get('price'),
            image_urls=item.get('image_urls')
        )

        # try:
        #     self.session.add(hotel)
        #     self.session.commit()
        # except Exception as e:
        #     self.session.rollback()
        #     spider.logger.error(f"Error saving item: {e}")
        
        return item

    def clean_data(self, item):
        """Perform any data cleaning here."""
        item['title'] = item.get('title', '').strip()
        item['rating'] = item.get('rating', '').strip()
        item['reviews_count'] = item.get('reviews_count', '').strip()
        item['location'] = [loc.strip() for loc in item.get('location', [])]
        item['room_type'] = item.get('room_type', '').strip()
        item['price'] = item.get('price', '').strip()
        item['image_urls'] = [url.strip() for url in item.get('image_urls', [])]
        return item
