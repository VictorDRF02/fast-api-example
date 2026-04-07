from typing import TYPE_CHECKING

from app.mixin.soft_delete import SoftDeleteMixin
from app.mixin.timestamp import TimestampMixin

from app.models.base import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from app.models.blog import Blog


class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_tags"
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    blogs: Mapped[list["Blog"]] = relationship(
        "Blog",
        secondary="tbl_blog_tags",
        back_populates="tags",
    )
