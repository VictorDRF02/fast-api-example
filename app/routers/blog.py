from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.blog import BlogCreate, BlogResponse, BlogUpdate, TagIDList
from app.services.blog import BlogService

router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
)


@router.get("/", response_model=list[BlogResponse])
async def read_blogs(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
):
    try:
        service = BlogService(db)
        return await service.list(limit=limit, offset=offset, pagination=True)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{blog_id}", response_model=BlogResponse)
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        instance = await service.get(blog_id)
        if not instance:
            raise HTTPException(status_code=404, detail="Blog not found")
        return instance
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(payload: BlogCreate, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        return await service.create(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(blog_id: int, payload: BlogUpdate, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        return await service.update(blog_id, payload)
    except ValueError as exc:
        if str(exc) == "Element not found":
            raise HTTPException(status_code=404, detail="Blog not found")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{blog_id}")
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        is_deleted = await service.delete(blog_id)
        message = "Blog deleted successfully" if is_deleted else "No blog to delete"
        return {"detail": message}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/{blog_id}/tags/{tag_id}", response_model=BlogResponse)
async def add_tag_to_blog(blog_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        return await service.add_tag(blog_id, tag_id)
    except ValueError as exc:
        error_msg = str(exc)
        if "Blog not found" in error_msg:
            raise HTTPException(status_code=404, detail="Blog not found")
        if "Tag not found" in error_msg:
            raise HTTPException(status_code=404, detail="Tag not found")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{blog_id}/tags/{tag_id}", response_model=BlogResponse)
async def remove_tag_from_blog(blog_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        return await service.remove_tag(blog_id, tag_id)
    except ValueError as exc:
        error_msg = str(exc)
        if "Blog not found" in error_msg:
            raise HTTPException(status_code=404, detail="Blog not found")
        if "Tag not found" in error_msg:
            raise HTTPException(status_code=404, detail="Tag not found")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/{blog_id}/tags", response_model=BlogResponse)
async def set_blog_tags(blog_id: int, payload: TagIDList, db: AsyncSession = Depends(get_db)):
    try:
        service = BlogService(db)
        return await service.set_tags(blog_id, payload.tag_ids)
    except ValueError as exc:
        error_msg = str(exc)
        if "Blog not found" in error_msg:
            raise HTTPException(status_code=404, detail="Blog not found")
        if "tags not found" in error_msg:
            raise HTTPException(status_code=404, detail="One or more tags not found")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
