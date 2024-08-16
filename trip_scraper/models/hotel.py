
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()

# Get the DATABASE_URL from the environment
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    hotelId = Column(Integer, primary_key=True)
    hotelName = Column(String(255), nullable=False)
    description = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    rating = Column(Float)
    amenities=Column(String) 
    images = Column(Text)  # Store image URLs as a comma-separated string
    address = Column(String(255))
    cityName = Column(String(255))


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

