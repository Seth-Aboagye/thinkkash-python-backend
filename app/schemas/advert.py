from pydantic import BaseModel

class AdvertCreate(BaseModel):
    company_name: str | None = None
    video_url: str
    amount_paid: float
    advert_duration_seconds: int = 0
