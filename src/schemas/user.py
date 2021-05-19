from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from src.schemas.rating import Rating


class UserBaseSchema(BaseModel):
    full_name: str
    email: EmailStr

class UserSchema(UserBaseSchema):
    id: int
    is_active: bool
    rates: List[Rating]

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserTokenizedSchema(BaseModel):
    user: Optional[dict]
    access_token: Optional[str]


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
