from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.movie import Movie


class CRUDMovie:

    def get_movies(self, db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Return list of movies with pagination arguments"""
        return db.query(Movie).offset(skip).limit(limit).all()


movies = CRUDMovie()
