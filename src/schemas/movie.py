from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.schema import date

from src.schemas.rating import Rating


class Movie(BaseModel):
    id: int
    imdb_id: str
    title: str
    genres: str
    release_date: date
    overview: str
    vote_average: float
    vote_count: int

    rates: List[Rating] = []

    class Config:
        orm_mode = True
