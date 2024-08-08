import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TripSpider(scrapy.Spider):
    name = "trip_spider"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Path to npm-installed ChromeDriver
        chromedriver_path = '/home/w3e63/Desktop/w3 assignment/scrapy/node/node_modules/chromedriver/bin/chromedriver'
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the WebDriver with the ChromeDriver path
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    def parse(self, response):
        # self.driver.get(response.url)
        
        # # Wait until the main-topic h1 is present (use appropriate waiting strategy)
        #  # Extract the h1 element with class name 'main-topic'
        # main_topic = response.css("h3.boundCities_title").get()

        # # Yield the result as an item
        # yield {
        #     'main_topic': main_topic
        # }
                # Wait until the page is fully loaded (use appropriate waiting strategy)
        self.driver.implicitly_wait(10)
        
        # Find the h3 element with the specific class name
        h3_elements = self.driver.find_elements(By.CLASS_NAME, "boundCities_title")
        
        for h3 in h3_elements:
            print(f"H3 Text: {h3.text}")
        
        # Close the browser
        self.driver.quit()
