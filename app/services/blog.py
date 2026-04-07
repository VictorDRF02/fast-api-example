from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.blog import Blog
from app.models.tag import Tag
from app.services.base import BaseService


class BlogService(BaseService[Blog]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Blog)

    async def add_tag(self, blog_id: int, tag_id: int) -> Blog:
        """Add a tag to a blog."""
        blog, tag = await self.get_tags_blog(blog_id, tag_id)

        if tag not in blog.tags:
            blog.tags.append(tag)
            await self.db.commit()
            await self.db.refresh(blog)

        return blog

    async def remove_tag(self, blog_id: int, tag_id: int) -> Blog:
        """Remove a tag from a blog."""
        blog, tag = await self.get_tags_blog(blog_id, tag_id)

        if tag in blog.tags:
            blog.tags.remove(tag)
            await self.db.commit()
            await self.db.refresh(blog)

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
        await self.db.refresh(blog)

        return blog

    async def get_tags_blog(self, blog_id: int, tag_id: int) -> tuple[Blog, Tag | None]:
        blog = await self.get(blog_id)
        if not blog:
            raise ValueError("Blog not found")

        query = select(Tag).where(Tag.id == tag_id)
        result = await self.db.execute(query)
        tag = result.scalar_one_or_none()
        if not tag:
            raise ValueError("Tag not found")

        return blog, tag