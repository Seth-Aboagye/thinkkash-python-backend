from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    video_url: Mapped[str] = mapped_column(String(500))
    content_duration_seconds: Mapped[int]
    advert_duration_seconds: Mapped[int] = mapped_column(default=0)
    total_duration_seconds: Mapped[int]
    likes: Mapped[int] = mapped_column(default=0)
    views: Mapped[int] = mapped_column(default=0)
    earnings: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
