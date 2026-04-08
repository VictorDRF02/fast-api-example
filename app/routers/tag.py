from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.tag import TagService

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)


@router.get("/", response_model=list[TagResponse])
async def read_tags(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
):
    try:
        service = TagService(db)
        return await service.list(limit=limit, offset=offset, pagination=True)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = TagService(db)
        instance = await service.get(tag_id)
        if not instance:
            raise HTTPException(status_code=404, detail="Tag not found")
        return instance
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(payload: TagCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        service = TagService(db)
        return await service.create(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, payload: TagUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        service = TagService(db)
        return await service.update(tag_id, payload)
    except ValueError as exc:
        if str(exc) == "Element not found":
            raise HTTPException(status_code=404, detail="Tag not found")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        service = TagService(db)
        is_deleted = await service.delete(tag_id)
        message = "Tag deleted successfully" if is_deleted else "No tag to delete"
        return {"detail": message}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

