from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_current_user, require_roles
from app.models.user import User
from app.models.video import Video
from app.schemas.video import VideoCreate

router = APIRouter()

@router.post("")
def create_video(payload: VideoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.content_duration_seconds > 100:
        raise HTTPException(status_code=400, detail="Uploader content cannot exceed 100 seconds")
    total = payload.content_duration_seconds + payload.advert_duration_seconds
    if payload.advert_duration_seconds > 50 or total > 150:
        raise HTTPException(status_code=400, detail="Total video composition exceeds allowed length")
    video = Video(
        user_id=current_user.id,
        title=payload.title,
        video_url=payload.video_url,
        content_duration_seconds=payload.content_duration_seconds,
        advert_duration_seconds=payload.advert_duration_seconds,
        total_duration_seconds=total,
        status="pending",
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

@router.get("/feed")
def feed(db: Session = Depends(get_db)):
    return db.query(Video).filter(Video.status == "approved").order_by(Video.created_at.desc()).all()

@router.post("/{video_id}/like")
def like_video(video_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    video = db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.likes += 1
    db.commit()
    return {"success": True, "likes": video.likes}

@router.post("/{video_id}/view")
def view_video(video_id: int, db: Session = Depends(get_db)):
    video = db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.views += 1
    db.commit()
    return {"success": True, "views": video.views}
