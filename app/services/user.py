from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db: AsyncSession):
        return await super().update(user_id, user)
