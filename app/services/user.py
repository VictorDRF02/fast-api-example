from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def create(self, user: UserCreate) -> User:
        instance = User(name=user.name, email=user.email)
        self.db.add(instance)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("EMAIL_EXISTS")

        await self.db.refresh(instance)
        return instance