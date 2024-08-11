
# Trip Scraper


This Trip Scraper project involves building a Scrapy web crawler that fetches location data from an AJAX API, selects a random place, and scrapes hotel details like title, photos, rating, latitude, longitude, room type, price, and city. The scraped data is saved in a PostgreSQL database using SQLAlchemy.



## Table of Contents
1. [Project Overview](#Project-Overview)
2. [Features](#Features)
3. [Project Structure](#Project-Structure)
4. [Installation](#Installation)
5. [Configuration](#Configuration)
6. [Data Model](#Data-Model)
7. [Database Setup](#Database-Setup)
8. [Scrapy Settings](#Scrapy-Settings)
9. [Running the Scraper](#Running-the-Scraper)
10. [Dependencies](#Dependencies)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview
The Trip Scraper project is designed to gather detailed information about hotels in various locations. It utilizes the Scrapy framework for web scraping and stores the collected data in a PostgreSQL database. The main focus of the scraper is on extracting hotel information such as:

- Title
- Images
- Rating
- Latitude and Longitude
- Location
- Room Type
- Price
- City

## Features
- Scrapes hotel data from multiple locations.
- Stores data in a PostgreSQL database using SQLAlchemy.
- Handles dynamic content loading via AJAX.
- Extracts images and saves them locally.
- Configurable settings for scraping and database connection

## Project Structure
```
trip_scraper/
├── scrapy.cfg               # Scrapy project configuration file
├── requirements.txt         # Python package dependencies
├── .gitignore               # Git ignore file
├── README.md                # Project README file
├── .env                     # Contains environment variables, including database connection url.        
├── trip_scraper/            # Main Scrapy project directory
│   ├── __init__.py
│   ├── items.py             # Item definitions for scraped data
│   ├── middlewares.py       # Middleware components for Scrapy
│   ├── pipelines.py         # Pipelines for processing scraped data
│   ├── settings.py          # Project settings for Scrapy
│   ├── spiders/             # Directory for spider definitions
│   │   ├── __init__.py
│   │   └── trip_spider.py   # Main spider for scraping hotels
│   ├── models/              # Directory for database models
│   │   ├── __init__.py
│   │   └── hotel.py         # SQLAlchemy model for hotel data
│   └── utils/               # Utility scripts
│       ├── __init__.py
│       ├── database.py      # Database initialization and connection
├── images/                  # Directory to store downloaded which create automatically

````

## Installation
### Prerequisites
- Python 3.8+
- PostgreSQL


1. Clone the repository:
`git clone https://github.com/yourusername/trip_scraper.git`

`cd trip_scraper`

2. Create and activate a virtual environment:
- Windows
`python -m venv env`

`source env/scripts/activate`
- macOS/Linux:
`python3 -m venv env`

`source env/bin/activate`

3. Install the dependencies:

`pip install -r requirements.txt`

## Data Model
The Hotel model in trip_scraper/models/hotel.py defines the structure of the data being scraped and stored:

- title
- rating
- reviews_count
- location
- latitude
- longitude
- room_type
- price
- image_urls
- city


## Database Setup
When project run database will automatically create Database. Create .env file and place DATABASE_URI

`DATABASE_URI = 'postgresql://username:password@localhost:port/database_name'`

## Scrapy Settings
You can configure the Scrapy settings in trip_scraper/settings.py to customize the scraping behavior, such as user agents, download delays, and pipelines.

## Running the Scraper
To run the scraper and start collecting hotel data, use the following command:

`scrapy crawl trip_spider`

## Dependencies
The project dependencies are listed in the requirements.txt file. They include:

- Scrapy
- SQLAlchemy
- psycopg2-binary
- geopy

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.