from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.orm import relationship

from src.database import db_base


class Movie(db_base):  # parrent
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    imdb_id = Column(String)
    title = Column(String)
    genres = Column(String)
    release_date = Column(Date)
    overview = Column(String)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    poster_path = Column(String)

    # bidirectional relationship in one-to-many
    rates = relationship("Rating", back_populates="movie")
