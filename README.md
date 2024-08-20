
# Trip Scraper


This Trip Scraper project involves building a Scrapy web crawler that fetches location data from an AJAX API, selects a random place, and scrapes hotel details like title, photos, rating, latitude, longitude, room type, price, and city. The scraped data is saved in a PostgreSQL database using SQLAlchemy.



## Table of Contents
1. [Project Overview](#Project-Overview)
2. [Features](#Features)
3. [Project Structure](#Project-Structure)
4. [Installation](#Installation)
5. [Configuration](#Configuration)
6. [Database Setup](#Database-Setup)
7. [Data Model](#Data-Model)
8. [Running the Scraper](#Running-the-Scraper)
9. [Dependencies](#Dependencies)


## Project Overview
The Trip Scraper project is designed to gather detailed information about hotels in various locations. It utilizes the Scrapy framework for web scraping and stores the collected data in a PostgreSQL database. The main focus of the scraper is on extracting hotel information such as:

- hotelName 
- description
- latitude 
- longitude 
- rating 
- amenities 
- images 
- address 
- cityName 

## Features
- Scrapes hotel data from multiple locations.
- Stores data in a PostgreSQL database using SQLAlchemy.
- Handles dynamic content loading via AJAX.
- Extracts images and saves them locally.
- Configurable settings for scraping and database connection

## Project Structure
```
trip_scraper/
├── scrapy.cfg             
├── requirements.txt        
├── .gitignore              
├── README.md              
├── .env.sample                     
├── trip_scraper/            
│   ├── __init__.py
│   ├── items.py            
│   ├── middlewares.py       
│   ├── pipelines.py         
│   ├── settings.py         
│   ├── spiders/             
│   │   ├── __init__.py
│   │   └── trip_spider.py   
│   ├── models/              
│       ├── __init__.py
│       └── hotel.py                        
│      
│            
├── images/                  

````

## Installation
### Prerequisites
- Python 3.8+
- PostgreSQL


1. Clone the repository:

``` bash
git clone https://github.com/samayunPathan/Scrapy-assignment.git
```

``` bash
cd trip_scraper
```

2. Create and activate a virtual environment:

- Windows
``` bash 
python -m venv env
```

``` bash
source env/scripts/activate
```
- macOS/Linux:

``` bash 
python3 -m venv env
```

``` bash 
source env/bin/activate
``` 

3. Install the dependencies:

``` bash 
pip install -r requirements.txt
```



## Database Setup
When project run database will automatically create Database. Create .env file and place DATABASE_URI

`DATABASE_URI = 'postgresql://username:password@localhost:port/database_name'`


## Running the Scraper
To run the scraper and start collecting hotel data, use the following command:

``` bash 
scrapy crawl trip_spider
```

## Data Model

The Hotel model in trip_scraper/models/hotel.py defines the structure of the data being scraped and stored:

- hotelName 
- description
- lat
- lon
- rating 
- amenities 
- images 
- address 
- cityName 

## Dependencies
The project dependencies are listed in the requirements.txt file. They include:

- scrapy 
- sqlalchemy
- psycopg2-binary
- python-dotenv

