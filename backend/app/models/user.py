from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .profile import Profile
    from .financial_goals import FinancialGoal


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    financial_goals: Mapped[list["FinancialGoal"]] = relationship(back_populates="user")
