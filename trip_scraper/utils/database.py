from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip_scraper.models.hotel import Base

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/scrap_data"

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