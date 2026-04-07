from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tag import TagResponse
from app.schemas.user import UserResponse

class BlogBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Annotated[str, Field(min_length=2, max_length=100)]
    content: Annotated[str, Field(min_length=1, max_length=1000)]
    user_id: Annotated[int, Field(gt=0)]


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=2, max_length=100)] = None
    content: Annotated[str | None, Field(default=None, min_length=1, max_length=1000)] = None
    user_id: Annotated[int | None, Field(default=None, gt=0)] = None


class BlogResponse(BlogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse]
    user: UserResponse


class TagIDList(BaseModel):
    tag_ids: list[int]