from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    rating = Column(Float)
    reviews_count = Column(String)
    location = Column(String)
    latitude= Column(Float)
    longitude=Column(Float)
    room_type = Column(String)
    price = Column(String)
    image_urls = Column(String)
    city = Column(String)

    def __repr__(self):
        return f"<Hotel(title='{self.title}', rating={self.rating}, price='{self.price}')>"