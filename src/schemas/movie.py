from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.schema import date


class MovieSchema(BaseModel):
    id: int
    imdb_id: str
    title: str
    genres: str
    release_year: Optional[str]
    release_date: Optional[date]
    overview: Optional[str]
    budget: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    user_rating: Optional[float]
    popularity: Optional[float]
    poster_url: Optional[str]

    # rates: List[Rating] = []

    class Config:
        orm_mode = True
