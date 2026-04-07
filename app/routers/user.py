from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserResponse])
async def read_users(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
):
    try:
        service = UserService(db)
        return await service.list(limit=limit, offset=offset, pagination=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = UserService(db)
        return await service.get(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        payload: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        service = UserService(db)
        return await service.create(payload)
    except ValueError as exc:
        if str(exc) == "EMAIL_EXISTS":
            raise HTTPException(status_code=409, detail="Email already exists")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate,
                      db: AsyncSession = Depends(get_db)):
    try:
        service = UserService(db)
        return await service.update(user_id, payload)
    except ValueError as exc:
        if str(exc) == "EMAIL_EXISTS":
            raise HTTPException(status_code=409, detail="Email already exists")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = UserService(db)
        is_deleted = await service.delete(user_id)
        message = "User deleted successfully" if is_deleted else "No user to delete"
        return {"detail": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
