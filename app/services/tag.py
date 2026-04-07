from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog import Tag
from app.services.base import BaseService


class TagService(BaseService[Tag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Tag)