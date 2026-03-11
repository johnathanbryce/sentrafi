from __future__ import annotations
from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction


class SyncBatch(Base):
    __tablename__ = "sync_batches"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # source file metadata
    source_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    # SHA-256 hex digest of raw PDF bytes — used to detect duplicate uploads
    source_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # processing status: "pending" (uploaded, awaiting Ollama), "completed", "failed"
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    # populated only on status="failed" — describes why processing failed
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    # total transactions extracted by Ollama — set when status moves to "completed"
    transaction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="sync_batches")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="batch")
