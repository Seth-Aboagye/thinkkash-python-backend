from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, require_roles
from app.models.advert import Advert, AdvertMapping, CreatorRewardRule
from app.models.video import Video
from app.schemas.advert import AdvertCreate
from app.services.advert_service import map_advert_first_come_first_served, calculate_creator_reward
from app.services.wallet_service import credit_wallet

router = APIRouter()

@router.post("")
def create_advert(payload: AdvertCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("advertiser", "admin"))):
    if payload.advert_duration_seconds > 50:
        raise HTTPException(status_code=400, detail="Advert duration cannot exceed 50 seconds")
    advert = Advert(
        advertiser_id=current_user.id,
        company_name=payload.company_name,
        video_url=payload.video_url,
        amount_paid=payload.amount_paid,
        status="active",
    )
    db.add(advert)
    db.commit()
    db.refresh(advert)
    video = map_advert_first_come_first_served(db, advert)
    return {"advert": advert, "mapped_video": video}

@router.get("/mappings")
def mappings(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(AdvertMapping).order_by(AdvertMapping.mapped_at.desc()).all()

@router.post("/monetize/{video_id}")
def monetize(video_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    video = db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    advert = db.query(Advert).filter(Advert.mapped_video_id == video_id).order_by(Advert.created_at.desc()).first()
    if not advert:
        raise HTTPException(status_code=404, detail="No monetizable advert linked to this video")
    reward = calculate_creator_reward(db, video.likes, video.views, float(advert.amount_paid))
    credit_wallet(db, video.user_id, reward["creator_reward"], "creator_reward", video.id, "Advert monetization")
    video.earnings = float(video.earnings) + reward["creator_reward"]
    db.commit()
    return {"video_id": video.id, **reward}
