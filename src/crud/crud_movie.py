from typing import List, Optional

from sqlalchemy import and_, func, desc
from sqlalchemy.orm import Session

from src.models import Rating, User
from src.models import movie
from src.models.movie import Movie

import pandas as pd

class CRUDMovie:
    def get_movie(self, db: Session, movie_id: int) -> Movie:
        """ Return specific movie by id """
        return db.query(Movie).filter(Movie.id == movie_id).first()

    def get_movie_with_rate(self, db: Session, movie_id: int, user_id: int) -> dict:
        """ Return specific movie by id with rate from specific user """
        return db.query(Movie, Rating.rating)\
            .filter(Movie.id == movie_id)\
            .outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == user_id))\
            .first()

    def get_movies(self, db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Return list of movies with pagination arguments"""
        return db.query(Movie).offset(skip).limit(limit).all()

    def get_movies_by_list_id(self, db: Session, movie_id_list: list) -> List[Movie]:
        return db.query(Movie).filter(Movie.id.in_(movie_id_list)).all()

    def search_movies_by_title(self, db: Session, search_string: str) -> Optional[List[Movie]]:
        movies = db.query(Movie).filter(Movie.title.contains(search_string)).limit(100).all()
        return movies

    def search_movies_by_title_with_rate(self, db: Session, search_string: str, user_id: int) -> List[dict]:
        movies_rate_tuple = db.query(Movie, Rating.rating)\
            .filter(Movie.title.contains(search_string))\
            .outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == user_id))\
            .limit(100)\
            .all()

        # df = pd.DataFrame(movies_rate_tuple, columns=['movie', 'user_rate'])
        # print(df.head())\
        # print(df['movie'].head())

        # movies = df['movie']
        # df = df[df['movie'].poster_url == 'a']
        # df = df[df['movie']['poster_url'] == 'a']
        # df = df['movie'].apply(lambda m: m['poster_url'] == 'a')
        # df = df.stack()[df.stack().apply(lambda x: x['poster_url'] == 'a')].unstack()
        # print(df.head())

        return movies_rate_tuple

    def latest_movie_id_watched_by_user(self, db: Session, user_id: int) -> int:
        rating = db.query(Rating) \
            .filter(Rating.user_id == user_id) \
            .order_by(desc(Rating.time_stamp)).limit(1)\
            .first()

        # subquery reduced :)
        # subqry = db.query(func.max(Rating.time_stamp)).filter(Rating.user_id == user_id)
        # qry = db.query(Rating).filter(Rating.user_id == user_id, Rating.time_stamp == subqry)
        return rating.movie_id


crud_movie = CRUDMovie()
