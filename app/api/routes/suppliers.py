from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_current_user, require_roles
from app.models.user import User
from app.models.supplier import SupplierProfile, SupplierDocument, SupplyOffer, SupplyShipment
from app.schemas.supplier import SupplierProfileCreate, SupplierDocumentCreate, SupplyOfferCreate
from app.services.shipment_service import generate_tracking_code

router = APIRouter()

@router.post("/profile")
def create_profile(payload: SupplierProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("supplier"))):
    profile = SupplierProfile(
        user_id=current_user.id,
        supplier_type=payload.supplier_type,
        business_name=payload.business_name,
        registration_number=payload.registration_number,
        tax_id=payload.tax_id,
        approval_status="pending",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/documents")
def upload_document(payload: SupplierDocumentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("supplier"))):
    profile = db.query(SupplierProfile).filter(SupplierProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Create supplier profile first")
    doc = SupplierDocument(supplier_id=profile.id, document_type=payload.document_type, document_url=payload.document_url)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.post("/offers")
def create_offer(payload: SupplyOfferCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("supplier"))):
    profile = db.query(SupplierProfile).filter(SupplierProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Supplier profile not found")
    offer = SupplyOffer(
        project_id=payload.project_id,
        supplier_id=profile.id,
        vendor_id=payload.vendor_id,
        item_name=payload.item_name,
        quantity=payload.quantity,
        unit=payload.unit,
        unit_price=payload.unit_price,
        total_price=payload.quantity * payload.unit_price,
        expected_delivery_date=payload.expected_delivery_date,
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    shipment = SupplyShipment(
        supply_offer_id=offer.id,
        origin_location=payload.origin_location,
        destination_location=payload.destination_location,
        tracking_code=generate_tracking_code(),
        courier_name=payload.courier_name,
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return {"offer": offer, "shipment": shipment}

@router.get("/my-supplies")
def my_supplies(db: Session = Depends(get_db), current_user: User = Depends(require_roles("supplier"))):
    profile = db.query(SupplierProfile).filter(SupplierProfile.user_id == current_user.id).first()
    if not profile:
        return []
    return db.query(SupplyOffer).filter(SupplyOffer.supplier_id == profile.id).all()

@router.get("/track/{tracking_code}")
def track(tracking_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    shipment = db.query(SupplyShipment).filter(SupplyShipment.tracking_code == tracking_code).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Tracking code not found")
    return shipment
