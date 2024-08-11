from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip_scraper.models.hotel import Base
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.drop_all(bind=engine)  # This will drop all existing tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()