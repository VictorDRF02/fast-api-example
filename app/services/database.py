from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseService:
    def __init__(self, db: AsyncSession):
        self.db = db
