from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, require_roles
from app.models.user import User
from app.models.video import Video
from app.models.supplier import SupplierProfile
from app.models.investor import InvestorProfile
from app.models.advert import CreatorRewardRule

router = APIRouter()

@router.get("/users")
def users(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(User).order_by(User.created_at.desc()).all()

@router.patch("/videos/{video_id}/approve")
def approve_video(video_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    video = db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.status = "approved"
    db.commit()
    return video

@router.patch("/suppliers/{supplier_id}/approve")
def approve_supplier(supplier_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    supplier = db.get(SupplierProfile, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier.approval_status = "approved"
    db.commit()
    return supplier

@router.patch("/investors/{investor_id}/approve")
def approve_investor(investor_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    investor = db.get(InvestorProfile, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    investor.approval_status = "approved"
    db.commit()
    return investor

@router.post("/reward-rules/seed")
def seed_reward_rules(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    if db.query(CreatorRewardRule).count() == 0:
        db.add_all([
            CreatorRewardRule(min_likes=500, min_views=0, payout_percent=15),
            CreatorRewardRule(min_likes=500, min_views=500, payout_percent=25),
            CreatorRewardRule(min_likes=1000000, min_views=1000000, payout_percent=50),
        ])
        db.commit()
    return {"success": True}
