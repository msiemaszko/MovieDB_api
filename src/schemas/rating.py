from pydantic import BaseModel, EmailStr, Field


class RatingCreateSchema(BaseModel):
    movie_id: int
    user_id: int
    rating: float


class RatingSchema(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float
    time_stamp: str

    class Config:
        orm_mode = True
