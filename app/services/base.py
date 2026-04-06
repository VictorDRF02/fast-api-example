from datetime import datetime, timezone
from typing import Generic, TypeVar, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.mixni.soft_delete import SoftDeleteMixin
from app.models.base import Base

# Generic type variable for SQLAlchemy models
T = TypeVar("T", bound=Base)

class BaseService(Generic[T]):
    """
    Base service class for common database operations.
    Attributes:
        db (Session): The database session.
        model (type[T]): The SQLAlchemy model class.
    """

    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model


    async def list(self, limit: int = 10, offset: int = 0, pagination: bool = True) -> Sequence[T]:
        """
        Generic list method. Accept limit, offset and the option to remove pagination.
        Args:
            limit (int, optional): The maximum number of items to return. Defaults to 10.
            offset (int, optional): The offset to return from the beginning of the list. Defaults to 0.
            pagination (bool, optional): Whether to return a pagination. Defaults to True.
        """
        query = select(self.model)
        if pagination:
            query = query.offset(offset).limit(limit)

        return (await self.db.execute(query)).scalars().all()


    async def get(self, element_id: int) -> T | None:
        """ Generic get method to get by the element id. """
        query = select(self.model).where(self.model.id == element_id)
        return (await self.db.execute(query)).scalar_one_or_none()


    async def delete(self, element_id: int) -> bool:
        """ Generic delete method to delete the element by id. Handles soft-delete models. """
        model = await self.get(element_id)

        if not model:
            return False

        if isinstance(model, SoftDeleteMixin):
            if not model.is_deleted:
                model.deleted_at = datetime.now(timezone.utc)
        else:
            await self.db.delete(model)

        await self.db.commit()
        return True