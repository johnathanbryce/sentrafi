from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, Text, DateTime, Numeric, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid4
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # identity
    profession: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # income (optional — user can sync statements without providing these)
    annual_salary: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True
    )
    pay_frequency: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, default="biweekly"
    )

    # location & currency (optional — enhances tax and financial analysis)
    country: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    province_or_state: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    currency: Mapped[Optional[str]] = mapped_column(
        String(3), nullable=True, default="USD"
    )

    # free-text context for LLM analysis (validated to 500 chars at API level)
    additional_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="profile")
