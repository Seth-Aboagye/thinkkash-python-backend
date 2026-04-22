from datetime import date
from pydantic import BaseModel

class SettlementItemIn(BaseModel):
    beneficiary_user_id: int
    beneficiary_role: str
    amount: float
    notes: str | None = None

class SettlementBatchIn(BaseModel):
    settlement_type: str
    period_start: date
    period_end: date
    items: list[SettlementItemIn]
