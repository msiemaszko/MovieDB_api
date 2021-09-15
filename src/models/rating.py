from sqlalchemy import (Column, Float, ForeignKey, Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship
from src.database import db_base


class Rating(db_base):  # children
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float)
    time_stamp = Column(Integer)

    # relacja film: wiele oscen do jednego filmu
    movie_id = Column(Integer, ForeignKey("movies.id"))
    movie = relationship("Movie", back_populates="rates")

    # relacja user: wiele ocen do jednego usera
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="rates")
