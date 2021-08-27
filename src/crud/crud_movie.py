from typing import List, Optional

from sqlalchemy import and_, func, desc
from sqlalchemy.orm import Session

from src.models import Rating, User
from src.models.movie import Movie


class CRUDMovie:
    def get_movie(self, db: Session, movie_id: int) -> Movie:
        """ Return specific movie by id """
        return db.query(Movie).filter(Movie.id == movie_id).first()

    @staticmethod
    def get_movie_with_rate(db: Session, movie_id: int, user_id: int) -> dict:
        """ Return specific movie by id with rate from specific user """
        return db.query(Movie, Rating.rating) \
            .filter(Movie.id == movie_id) \
            .outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == user_id)) \
            .first()

    def get_movies(self, db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Return list of movies with pagination arguments"""
        return db.query(Movie).offset(skip).limit(limit).all()

    def get_movies_by_list_id(self, db: Session, movie_id_list: list) -> List[Movie]:
        return db.query(Movie).filter(Movie.id.in_(movie_id_list)).all()

    def search_movies_by_title(self, db: Session, search_string: str) -> Optional[List[Movie]]:
        movies = db.query(Movie).filter(Movie.title.contains(search_string)).limit(100).all()
        return movies

    async def search_movies_by_title_with_rate(self, db: Session, search_string: str, user_id: int) -> List[dict]:
        return db.query(Movie, Rating.rating) \
            .filter(Movie.title.ilike(f'%{search_string}%')) \
            .outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == user_id)) \
            .limit(1000) \
            .all()

    def latest_movie_id_watched_by_user(self, db: Session, user_id: int) -> int:
        rating = db.query(Rating) \
            .filter(Rating.user_id == user_id) \
            .order_by(desc(Rating.time_stamp)).limit(1) \
            .first()

        # subquery reduced :)
        # subqry = db.query(func.max(Rating.time_stamp)).filter(Rating.user_id == user_id)
        # qry = db.query(Rating).filter(Rating.user_id == user_id, Rating.time_stamp == subqry)
        return rating.movie_id

    def get_movies_without_posters(self, count: int, db: Session) -> List[Movie]:
        return db.query(Movie).filter(func.coalesce(Movie.poster_url, '') == '').limit(count).all()

    def update_movie_poster_url(self, db: Session, movie_obj: Movie, poster_url: str):
        query = db.query(Movie)\
            .filter(Movie.id == movie_obj.id)\
            .update({'poster_url': poster_url})
        db.commit()
        return query


crud_movie = CRUDMovie()
