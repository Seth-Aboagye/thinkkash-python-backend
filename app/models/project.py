from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ProjectIdea(Base):
    __tablename__ = "project_ideas"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    raw_materials_needed: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_budget: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    funding_goal: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    funded_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    project_status: Mapped[str] = mapped_column(String(30), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
