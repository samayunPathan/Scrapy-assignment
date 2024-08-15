# In models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    hotelName = Column(String)
    description = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    rating = Column(Float)
    images = Column(ARRAY(String))
    address = Column(String)
    cityName = Column(String)

