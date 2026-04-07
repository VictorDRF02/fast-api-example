from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.blog import Blog
from app.models.tag import Tag
from app.services.model import ModelService


class BlogService(ModelService[Blog]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Blog)

    async def list(self, limit: int = 10, offset: int = 0, pagination: bool = True):
        """Override list to eager load tags and user."""
        query = select(self.model).options(
            selectinload(Blog.tags),
            selectinload(Blog.user)
        )
        if pagination:
            query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get(self, element_id: int) -> Blog | None:
        """Override get to eager load tags and user."""
        query = select(self.model).where(self.model.id == element_id).options(
            selectinload(Blog.tags),
            selectinload(Blog.user)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def add_tag(self, blog_id: int, tag_id: int) -> Blog:
        """Add a tag to a blog."""
        blog, tag = await self._get_blog_and_tag(blog_id, tag_id)

        if tag and tag not in blog.tags:
            blog.tags.append(tag)
            await self.db.commit()
            await self.db.refresh(blog, ["tags"])

        return blog

    async def remove_tag(self, blog_id: int, tag_id: int) -> Blog:
        """Remove a tag from a blog."""
        blog, tag = await self._get_blog_and_tag(blog_id, tag_id)

        if tag and tag in blog.tags:
            blog.tags.remove(tag)
            await self.db.commit()
            await self.db.refresh(blog, ["tags"])

        return blog

    async def set_tags(self, blog_id: int, tag_ids: list[int]) -> Blog:
        """Set tags for a blog (replaces existing tags)."""
        blog = await self.get(blog_id)
        if not blog:
            raise ValueError("Blog not found")

        # Fetch all tags
        query = select(Tag).where(Tag.id.in_(tag_ids))
        result = await self.db.execute(query)
        tags = result.scalars().all()

        if len(tags) != len(tag_ids):
            raise ValueError("One or more tags not found")

        blog.tags = list(tags)
        await self.db.commit()
        await self.db.refresh(blog, ["tags"])

        return blog

    async def _get_blog_and_tag(self, blog_id: int, tag_id: int) -> tuple[Blog | None, Tag | None]:
        """Helper to get blog and tag with eager loading."""
        blog = await self.get(blog_id)
        if not blog:
            raise ValueError("Blog not found")

        query = select(Tag).where(Tag.id == tag_id)
        result = await self.db.execute(query)
        tag = result.scalar_one_or_none()
        if not tag:
            raise ValueError("Tag not found")

        return blog, tag
