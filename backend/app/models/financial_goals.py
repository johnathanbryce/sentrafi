from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, DateTime, Date, Numeric, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class FinancialGoal(Base):
    __tablename__ = "financial_goals"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid4
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    target_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3
    )  # 1-5, default middle
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="financial_goals")
