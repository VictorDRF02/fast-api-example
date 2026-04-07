from typing import TYPE_CHECKING

from app.mixin.soft_delete import SoftDeleteMixin
from app.mixin.timestamp import TimestampMixin

from app.models.base import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from app.models.blog import Blog


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_users"
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    blogs: Mapped[list["Blog"]] = relationship("Blog", back_populates="user")
