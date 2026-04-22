from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class InvestorProfile(Base):
    __tablename__ = "investor_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    investor_type: Mapped[str] = mapped_column(String(30))
    business_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    risk_profile: Mapped[str | None] = mapped_column(String(30), nullable=True)
    approval_status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Investment(Base):
    __tablename__ = "investments"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project_ideas.id"))
    investor_id: Mapped[int] = mapped_column(ForeignKey("investor_profiles.id"))
    amount: Mapped[float] = mapped_column(Numeric(14, 2))
    investment_status: Mapped[str] = mapped_column(String(30), default="active")
    expected_return_percent: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    actual_return_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    invested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
