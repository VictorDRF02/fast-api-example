from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

class SoftDeleteMixin:
    """Minix for adding soft delete functionality to models."""
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        default=None, 
        nullable=True
    )
    
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None