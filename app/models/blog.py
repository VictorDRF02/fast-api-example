from app.mixni.soft_delete import SoftDeleteMixin
from app.mixni.timestamp import TimestampMixin

from app.models.base import Base
from app.models.tag import Tag
from app.models.user import User

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Column, Table


class Blog(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_blogs"
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("tbl_users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="blogs")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary="tbl_blog_tags", back_populates="blogs")
 
    
# Association table for many-to-many relationship between Blog and Tag
blog_tag_association = Table(
    "tbl_blog_tags",
    Base.metadata,
    Column("blog_id", ForeignKey("tbl_blogs.id"), primary_key=True),
    Column("tag_id", ForeignKey("tbl_tags.id"), primary_key=True),
)