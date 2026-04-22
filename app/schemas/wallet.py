from pydantic import BaseModel

class WalletFundIn(BaseModel):
    amount: float
