from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, require_roles
from app.models.investor import InvestorProfile, Investment
from app.models.project import ProjectIdea
from app.schemas.investor import InvestorProfileCreate, InvestmentCreate

router = APIRouter()

@router.post("/profile")
def create_profile(payload: InvestorProfileCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("investor"))):
    profile = InvestorProfile(
        user_id=current_user.id,
        investor_type=payload.investor_type,
        business_name=payload.business_name,
        risk_profile=payload.risk_profile,
        approval_status="pending",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/invest")
def invest(payload: InvestmentCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("investor"))):
    profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Investor profile not found")
    inv = Investment(
        project_id=payload.project_id,
        investor_id=profile.id,
        amount=payload.amount,
        expected_return_percent=payload.expected_return_percent,
        investment_status="active",
    )
    db.add(inv)
    project = db.get(ProjectIdea, payload.project_id)
    if project:
        project.funded_amount = float(project.funded_amount) + payload.amount
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/portfolio")
def portfolio(db: Session = Depends(get_db), current_user = Depends(require_roles("investor"))):
    profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == current_user.id).first()
    if not profile:
        return []
    return db.query(Investment).filter(Investment.investor_id == profile.id).all()
