from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from src.database import db_base

class Movie(db_base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    imdb_id = Column(String)
    title = Column(String)
    genres = Column(String)
    release_date = Column(Date)
    overview = Column(String)

    rates = relationship("Rating", back_populates="to")
