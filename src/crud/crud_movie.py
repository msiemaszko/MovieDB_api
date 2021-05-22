from typing import List, Optional

from sqlalchemy.orm import Session

from src.models import Rating
from src.models.movie import Movie


class CRUDMovie:
    def get_movies(self, db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Return list of movies with pagination arguments"""
        return db.query(Movie).offset(skip).limit(limit).all()

    def search_movies_by_title(
        self, db: Session, search_string: str
    ) -> Optional[List[Movie]]:
        movies = db.query(Movie).filter(Movie.title.contains(search_string)).all()
        # .join(Rating)\
        return movies


crud_movies = CRUDMovie()