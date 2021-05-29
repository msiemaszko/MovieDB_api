import time
from typing import List

from sqlalchemy.orm import Session

from src.models import Rating, User
from src.schemas import RatingCreateSchema


class CRUDRates:
    def get_ratings(self, db: Session, skip: int = 0, limit: int = 100) -> List[Rating]:
        return db.query(Rating).offset(skip).limit(limit).all()

    def apply_user_rating(self, db: Session, req_rating: RatingCreateSchema) -> Rating:
        """Add new rating for specific movie, when exists then update"""
        exist_rating = (
            db.query(Rating)
            .filter(
                Rating.user_id == req_rating.user_id,
                Rating.movie_id == req_rating.movie_id,
            )
            .first()
        )
        if exist_rating:
            db_rating = exist_rating
            db_rating.rating = req_rating.rating  # overwrite rating
        else:
            db_rating = Rating(**req_rating.dict(), time_stamp=time.time())
            db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating


crud_rate = CRUDRates()
