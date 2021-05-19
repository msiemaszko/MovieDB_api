from sqlalchemy.orm import Session
from src import models

class CRUDRates:
    def get_ratings(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Rating).offset(skip).limit(limit).all()

rates = CRUDRates()
