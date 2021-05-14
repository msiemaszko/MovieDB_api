from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


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

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)