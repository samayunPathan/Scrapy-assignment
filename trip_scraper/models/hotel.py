# trip_scraper/models/hotel.py
from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for our models
Base = declarative_base()

# Define the Hotel model
class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    rating = Column(String)
    reviews_count = Column(String)
    location = Column(ARRAY(String))
    room_type = Column(String)
    price = Column(String)
    image_urls = Column(ARRAY(String))

# Define the PostgreSQL URL
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost/mydatabase"

# # Create an engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Create all tables
# Base.metadata.create_all(engine)

# # Create a session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
