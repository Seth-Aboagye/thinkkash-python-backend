from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, DateTime, Text, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class SupplierProfile(Base):
    __tablename__ = "supplier_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    supplier_type: Mapped[str] = mapped_column(String(30))
    business_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registration_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tax_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    approval_status: Mapped[str] = mapped_column(String(30), default="pending")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SupplierDocument(Base):
    __tablename__ = "supplier_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier_profiles.id"))
    document_type: Mapped[str] = mapped_column(String(100))
    document_url: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="pending")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SupplyOffer(Base):
    __tablename__ = "supply_offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project_ideas.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier_profiles.id"))
    vendor_id: Mapped[int]
    item_name: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[float] = mapped_column(Numeric(14, 2))
    unit: Mapped[str] = mapped_column(String(50))
    unit_price: Mapped[float] = mapped_column(Numeric(14, 2))
    total_price: Mapped[float] = mapped_column(Numeric(14, 2))
    offer_status: Mapped[str] = mapped_column(String(30), default="pending")
    expected_delivery_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SupplyShipment(Base):
    __tablename__ = "supply_shipments"

    id: Mapped[int] = mapped_column(primary_key=True)
    supply_offer_id: Mapped[int] = mapped_column(ForeignKey("supply_offers.id"))
    origin_location: Mapped[str | None] = mapped_column(Text, nullable=True)
    destination_location: Mapped[str | None] = mapped_column(Text, nullable=True)
    tracking_code: Mapped[str] = mapped_column(String(100), unique=True)
    courier_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shipment_status: Mapped[str] = mapped_column(String(30), default="preparing")
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
