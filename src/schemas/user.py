from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from src.schemas.rating import RatingSchema


class UserBaseSchema(BaseModel):
    full_name: str
    email: EmailStr


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool
    # rates: List[RatingSchema] = []

    class Config:
        orm_mode = True


# pomocnicze:
class UserCreateSchema(UserBaseSchema):
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserTokenizedSchema(BaseModel):
    user: UserSchema
    access_token: str
