import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    func,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from models.base import Base

if TYPE_CHECKING:
    from models.user import User


class Job(Base):
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4
    )
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_archived: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false()
    )
    deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false()
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    performer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )

    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    performer: Mapped["User"] = relationship(
        "User", foreign_keys=[performer_id]
    )

    @property
    def fullname(self) -> str:
        return self.title

    def __str__(self) -> str:
        return f"{self.id} - {self.fullname}"
