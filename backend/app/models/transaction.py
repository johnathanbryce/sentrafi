from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, Date, DateTime, Numeric, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .sync_batch import SyncBatch


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    # denormalized from sync_batches for direct indexed lookups —
    # nearly every query filters by user first (SQL Agent, sentra status, reports)
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    batch_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("sync_batches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # transaction data extracted by Ollama from statement markdown
    date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    # always stored as a positive value — direction indicated by transaction_type
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    # free-text category assigned by Ollama (e.g. "groceries", "rent", "salary")
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # "debit" (money out) or "credit" (money in)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)

    # used by `sentra audit --flagged` — lets users mark transactions for review
    is_flagged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="transactions")
    batch: Mapped["SyncBatch"] = relationship(back_populates="transactions")
