from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.services.wallet_service import ensure_wallet
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(payload.password)
    logger.warning(f"REGISTER email={payload.email} hash_prefix={hashed[:30]}")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hashed,
        phone=payload.phone,
        country=payload.country,
        role=payload.role,
        verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    ensure_wallet(db, user.id)
    return user

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        logger.warning(f"LOGIN email={payload.email} user_not_found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    verify_result = verify_password(payload.password, user.password_hash)
    logger.warning(
        f"LOGIN email={payload.email} "
        f"stored_hash_prefix={str(user.password_hash)[:30]} "
        f"verify_result={verify_result}"
    )

    if not verify_result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id), user.role)
    return {"access_token": token, "token_type": "bearer"}
