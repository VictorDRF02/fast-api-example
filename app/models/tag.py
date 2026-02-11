from app.mixni.soft_delete import SoftDeleteMixin
from app.mixni.timestamp import TimestampMixin

from app.models.base import Base

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_tags"
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)