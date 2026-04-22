from sqlalchemy.orm import Session
from app.models.advert import Advert, AdvertMapping, CreatorRewardRule
from app.models.video import Video

def map_advert_first_come_first_served(db: Session, advert: Advert):
    video = (
        db.query(Video)
        .filter(Video.status == "approved")
        .filter(~Video.id.in_(db.query(AdvertMapping.video_id)))
        .order_by(Video.created_at.asc())
        .first()
    )
    if not video:
        return None
    advert.mapped_video_id = video.id
    db.add(AdvertMapping(advert_id=advert.id, video_id=video.id))
    db.commit()
    db.refresh(advert)
    return video

def calculate_creator_reward(db: Session, likes: int, views: int, advert_paid_amount: float):
    rules = db.query(CreatorRewardRule).filter(CreatorRewardRule.is_active == True).all()
    payout_percent = 0
    for rule in rules:
        if likes >= rule.min_likes and views >= rule.min_views:
            payout_percent = float(rule.payout_percent)
    creator_reward = round(advert_paid_amount * payout_percent / 100, 2)
    thinkkash_retained = round(advert_paid_amount - creator_reward, 2)
    return {
        "payout_percent": payout_percent,
        "creator_reward": creator_reward,
        "thinkkash_retained": thinkkash_retained,
    }
