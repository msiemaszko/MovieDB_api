from pydantic import BaseModel, EmailStr, Field


class RatingCreate(BaseModel):
    user_id: int
    rating: float


class Rating(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float
    time_stamp: str

    class Config:
        orm_mode = True
