from sqlalchemy.orm import Session
from app.models.wallet import Wallet, WalletTransaction

def ensure_wallet(db: Session, user_id: int) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if wallet:
        return wallet
    wallet = Wallet(user_id=user_id)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet

def credit_wallet(db: Session, user_id: int, amount: float, source_type: str, reference_id: int | None = None, description: str | None = None):
    wallet = ensure_wallet(db, user_id)
    wallet.available_balance = float(wallet.available_balance) + amount
    db.add(WalletTransaction(
        wallet_id=wallet.id,
        transaction_type="credit",
        source_type=source_type,
        reference_id=reference_id,
        amount=amount,
        description=description,
    ))
    db.commit()
    db.refresh(wallet)
    return wallet
