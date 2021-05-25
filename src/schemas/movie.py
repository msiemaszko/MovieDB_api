from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.schema import date


class MovieSchema(BaseModel):
    id: int
    imdb_id: str
    title: str
    genres: str
    release_date: Optional[date]
    overview: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    user_rating: Optional[float]

    # rates: List[Rating] = []

    class Config:
        orm_mode = True
