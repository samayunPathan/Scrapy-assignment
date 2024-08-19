BOT_NAME = "trip_scraper"
SPIDER_MODULES = ["trip_scraper.spiders"]
NEWSPIDER_MODULE = "trip_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# ---- proxy setting ----- 
# DOWNLOADER_MIDDLEWARES = {
#     'trip_scraper.middlewares.CustomProxyMiddleware': 350,
# }

# Enable or configure middlewares if needed

DOWNLOADER_MIDDLEWARES = {
    'trip_scraper.middlewares.TripScraperMiddleware': 543,
}


ITEM_PIPELINES = {
    'trip_scraper.pipelines.TripScraperPipeline': 300,
}
