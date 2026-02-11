from app.mixni.soft_delete import SoftDeleteMixin
from app.mixni.timestamp import TimestampMixin

from app.models.base import Base
from app.models.user import User

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey


class Blog(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_blogs"
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("tbl_users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="blogs")
    