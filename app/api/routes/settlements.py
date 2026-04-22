from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, require_roles
from app.models.settlement import SettlementBatch, SettlementItem
from app.schemas.settlement import SettlementBatchIn
from app.services.wallet_service import credit_wallet

router = APIRouter()

@router.post("")
def create_batch(payload: SettlementBatchIn, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    batch = SettlementBatch(
        settlement_type=payload.settlement_type,
        period_start=payload.period_start,
        period_end=payload.period_end,
        total_amount=sum(i.amount for i in payload.items),
        created_by=current_user.id,
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    for item in payload.items:
        db.add(SettlementItem(
            batch_id=batch.id,
            beneficiary_user_id=item.beneficiary_user_id,
            beneficiary_role=item.beneficiary_role,
            amount=item.amount,
            notes=item.notes,
        ))
    db.commit()
    return batch

@router.get("")
def list_batches(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(SettlementBatch).order_by(SettlementBatch.created_at.desc()).all()

@router.post("/{batch_id}/process")
def process_batch(batch_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    batch = db.get(SettlementBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Settlement batch not found")
    items = db.query(SettlementItem).filter(SettlementItem.batch_id == batch_id).all()
    for item in items:
        credit_wallet(db, item.beneficiary_user_id, float(item.amount), "settlement_batch", batch_id, f"{batch.settlement_type} settlement")
        item.status = "paid"
    batch.status = "processed"
    db.commit()
    return {"success": True, "batch_id": batch_id, "processed_items": len(items)}
