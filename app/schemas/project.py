from pydantic import BaseModel

class ProjectCreate(BaseModel):
    video_id: int
    title: str
    description: str | None = None
    category: str | None = None
    raw_materials_needed: str | None = None
    estimated_budget: float = 0
    funding_goal: float

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    category: str | None = None
    funding_goal: float
    funded_amount: float
    project_status: str
