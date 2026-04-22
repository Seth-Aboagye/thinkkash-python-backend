from pydantic import BaseModel

class InvestorProfileCreate(BaseModel):
    investor_type: str
    business_name: str | None = None
    risk_profile: str | None = None

class InvestmentCreate(BaseModel):
    project_id: int
    amount: float
    expected_return_percent: float = 12
