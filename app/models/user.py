from app.mixni.soft_delete import SoftDeleteMixin
from app.mixni.timestamp import TimestampMixin
from app.models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tbl_users"
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)