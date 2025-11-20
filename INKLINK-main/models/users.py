from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    lastname: constr(min_length=1, max_length=100)
    email: EmailStr
    active: bool = True
    admin: bool = False


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=255)


class UserUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    lastname: Optional[constr(min_length=1, max_length=100)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=255)] = None
    active: Optional[bool] = None
    admin: Optional[bool] = None


class User(BaseModel):
    id: int
    name: str
    lastname: str
    email: EmailStr
    active: bool
    admin: bool

    class Config:
        orm_mode = True