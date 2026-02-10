from app.mixni.soft_delete import SoftDeleteMixin
from app.mixni.timestamp import TimestampMixin
from app.models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Blog(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_blogs"
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)