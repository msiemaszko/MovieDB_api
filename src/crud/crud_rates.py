from sqlalchemy.orm import Session

from src import models, schemas


class CRUDRates:
    def get_ratings(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Rating).offset(skip).limit(limit).all()

    def create_user_rating(
        db: Session, rating: schemas.rating.RatingCreate, movie_id: int
    ):
        db_rating = models.Raging(**rating.dict(), movie_id=movie_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating


rates = CRUDRates()
