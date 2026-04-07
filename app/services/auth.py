from datetime import datetime, UTC, timedelta

import jwt
from sqlalchemy import select

from app.models.user import User
from app.services.database import DatabaseService


class AuthService(DatabaseService):
    async def login(self, email: str, password: str):
        query = select(User).where(User.email == email)
        user = (await  self.db.execute(query)).scalar_one_or_none()
        if not user:
            raise ValueError("Invalid credentials")
        if user.password != password:
            raise ValueError("Invalid credentials")
        return self.getToken(user)

    async def register(self, email: str, password: str):
        # Implement registration logic here
        pass

    async def get_token(self, user: User) -> str:
        payload = {
            "sub": user.id,
            "name": user.name,
            "email": user.email,
            "iat": datetime.now(UTC),  # Issued At
            "exp": datetime.now(UTC) + timedelta(hours=12)  # Expiration
        }
        # TODO: Change secret key
        return jwt.encode(payload, '1234', algorithm="HS256")
