from datetime import datetime, UTC, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import Register, Login
from app.services.database import DatabaseService


class AuthService(DatabaseService):
    async def login(self, payload: Login) -> dict:
        email, password = payload.email , payload.password
        query = select(User).where(User.email == email)
        user = (await self.db.execute(query)).scalar_one_or_none()

        if not user or not password == user.password:
            raise ValueError("INVALID_CREDENTIALS")

        token = create_access_token(
            {"sub": str(user.id), "name": user.name, "email": user.email}
        )
        return {"access_token": token, "token_type": "bearer"}


    async def register(self, payload: Register) -> dict:
        name, email, password = payload.name, payload.email, payload.password
        existing = (await self.db.execute(select(User).where(User.email == email))).scalar_one_or_none()
        if existing:
            raise ValueError("EMAIL_EXISTS")

        user = User(
            name=name,
            email=email,
            password=password,
        )

        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("EMAIL_EXISTS")

        await self.db.refresh(user)

        token = create_access_token(
            {"sub": str(user.id), "name": user.name, "email": user.email}
        )
        return {"access_token": token, "token_type": "bearer"}
