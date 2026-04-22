from datetime import date
from pydantic import BaseModel

class SupplierProfileCreate(BaseModel):
    supplier_type: str
    business_name: str | None = None
    registration_number: str | None = None
    tax_id: str | None = None

class SupplierDocumentCreate(BaseModel):
    document_type: str
    document_url: str

class SupplyOfferCreate(BaseModel):
    project_id: int
    vendor_id: int
    item_name: str
    quantity: float
    unit: str
    unit_price: float
    expected_delivery_date: date | None = None
    origin_location: str | None = None
    destination_location: str | None = None
    courier_name: str | None = None
