from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_current_user
from app.models.user import User
from app.models.project import ProjectIdea
from app.schemas.project import ProjectCreate

router = APIRouter()

@router.post("")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = ProjectIdea(
        video_id=payload.video_id,
        creator_id=current_user.id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        raw_materials_needed=payload.raw_materials_needed,
        estimated_budget=payload.estimated_budget,
        funding_goal=payload.funding_goal,
        funded_amount=0,
        project_status="open",
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("")
def list_projects(db: Session = Depends(get_db)):
    return db.query(ProjectIdea).order_by(ProjectIdea.created_at.desc()).all()

@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(ProjectIdea, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
