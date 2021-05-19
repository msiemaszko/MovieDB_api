from sqlalchemy import Column, Integer, Float, Date, String, TIMESTAMP, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import db_base

class User(db_base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String) #, unique=True, index=True
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    rates = relationship("Rating", back_populates="owner")


class Rating(db_base):
    __tablename__ = 'ratings'
    __table_args__ = (UniqueConstraint('user_id', 'movie_id'),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)
    time_stamp = Column(String)

    owner = relationship("User", back_populates="rates")
    to = relationship("Movie", back_populates="rates")


class Movie(db_base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    imdb_id = Column(String)
    title = Column(String)
    genres = Column(String)
    release_date = Column(Date)
    overview = Column(String)

    rates = relationship("Rating", back_populates="to")
