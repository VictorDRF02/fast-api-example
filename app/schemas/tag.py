from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=2, max_length=50)]


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Annotated[str | None, Field(default=None, min_length=2, max_length=50)] = None


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

