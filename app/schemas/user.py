from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: Annotated[EmailStr, Field(max_length=100)]


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    id: int
    name: Annotated[str | None, Field(default=None, min_length=2, max_length=50)] = None
    email: Annotated[EmailStr | None, Field(default=None, max_length=100)] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

