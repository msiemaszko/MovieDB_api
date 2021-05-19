from sqlalchemy import Column, Integer, Float, Date, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from database import db_base

class User(db_base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String) #, unique=True, index=True
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # rates = relationship("Rating")

class Movie(db_base):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    imdb_id = Column(String)
    title = Column(String)
    genres = Column(String)
    release_date = Column(Date)
    overview = Column(String)

class Rating(db_base):
    __tablename__ = 'Rating'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    # user_id = relationship("User")
    movie_id = Column(Float)
    rating = Column(Float)
    time_stamp = Column(String)