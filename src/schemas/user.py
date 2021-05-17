from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from src.schemas.item import Item


class UserBaseSchema(BaseModel):
    full_name: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class UserTokenizedSchema(BaseModel):
    user: Optional[dict]
    access_token: Optional[str]


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
