from pydantic import BaseModel, EmailStr, Field

class Rating(BaseModel):
    id = int
    user_id = int
    movie_id = int
    rating = float
    time_stamp = str