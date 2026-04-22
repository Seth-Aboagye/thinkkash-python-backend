from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_current_user
from app.models.wallet import Wallet, WalletTransaction
from app.schemas.wallet import WalletFundIn
from app.services.wallet_service import ensure_wallet, credit_wallet

router = APIRouter()

@router.get("/me")
def my_wallet(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    wallet = ensure_wallet(db, current_user.id)
    transactions = db.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet.id).order_by(WalletTransaction.created_at.desc()).all()
    return {"wallet": wallet, "transactions": transactions}

@router.post("/fund")
def fund_wallet(payload: WalletFundIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    wallet = credit_wallet(db, current_user.id, payload.amount, "wallet_topup", None, "Manual top-up")
    return wallet
