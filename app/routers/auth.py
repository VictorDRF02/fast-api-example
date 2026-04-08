from fastapi import APIRouter, Depends, HTTPException
from fastapi_cloud_cli.commands.login import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import Login, Register
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenResponse)
async def login(payload: Login, db: AsyncSession = Depends(get_db)):
    try:
        service = AuthService(db)
        return await service.login(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post('/register', response_model=TokenResponse)
async def register(payload: Register, db: AsyncSession = Depends(get_db)):
    try:
        service = AuthService(db)
        return await service.register(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid registration details. The email may exists")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

