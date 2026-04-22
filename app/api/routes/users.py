from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.get("/me")
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "verified": current_user.verified,
    }
