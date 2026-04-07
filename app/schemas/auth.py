from typing import Annotated

from pydantic import BaseModel, Field, EmailStr

from app.schemas.user import UserBase


class Login(BaseModel):
    email: Annotated[str, Field(min_length=1)]
    password: Annotated[str, Field(min_length=1)]

class Register(UserBase):
    password: Annotated[EmailStr, Field(min_length=8)]

class Token(BaseModel):
    access_token: str
