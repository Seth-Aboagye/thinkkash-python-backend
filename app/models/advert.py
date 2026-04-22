from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Advert(Base):
    __tablename__ = "adverts"

    id: Mapped[int] = mapped_column(primary_key=True)
    advertiser_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    video_url: Mapped[str] = mapped_column(String(500))
    amount_paid: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    mapped_video_id: Mapped[int | None] = mapped_column(ForeignKey("videos.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AdvertMapping(Base):
    __tablename__ = "advert_mappings"

    id: Mapped[int] = mapped_column(primary_key=True)
    advert_id: Mapped[int] = mapped_column(ForeignKey("adverts.id"))
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"))
    mapped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    mapping_status: Mapped[str] = mapped_column(String(30), default="active")

class CreatorRewardRule(Base):
    __tablename__ = "creator_reward_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    min_likes: Mapped[int] = mapped_column(default=0)
    min_views: Mapped[int] = mapped_column(default=0)
    payout_percent: Mapped[float] = mapped_column(Numeric(5, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
