from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class SettlementBatch(Base):
    __tablename__ = "settlement_batches"

    id: Mapped[int] = mapped_column(primary_key=True)
    settlement_type: Mapped[str] = mapped_column(String(50))
    period_start: Mapped[datetime] = mapped_column(Date)
    period_end: Mapped[datetime] = mapped_column(Date)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SettlementItem(Base):
    __tablename__ = "settlement_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("settlement_batches.id"))
    beneficiary_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    beneficiary_role: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(String(30), default="pending")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
