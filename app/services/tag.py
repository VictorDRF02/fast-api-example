from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog import Tag
from app.services.model import ModelService


class TagService(ModelService[Tag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Tag)