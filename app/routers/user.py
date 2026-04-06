from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse
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
async def read_user(user_id: int):
    pass


@router.post("/")
async def create_user():
    pass


@router.put("/{user_id}")
async def update_user(user_id: int):
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    pass
