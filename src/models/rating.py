from sqlalchemy import Column, Integer, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database import db_base

class Rating(db_base):
    __tablename__ = 'ratings'
    __table_args__ = (UniqueConstraint('user_id', 'movie_id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    # movie_id = Column(Integer)
    rating = Column(Float)
    time_stamp = Column(String)

    owner = relationship("User", back_populates="rates")
    to = relationship("Movie", back_populates="rates")