from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.model import ModelService


class UserService(ModelService[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
