from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import Dump
from ..services.llm import generate_bundle
from pydantic import BaseModel, Field

router = APIRouter(prefix="/dumps", tags=["dumps"])

class DumpIn(BaseModel):
    text: str = Field(min_length=4)
    tags: Optional[List[str]] = None

class DumpOut(BaseModel):
    id: int
    action_plan: str
    wellness_tip: str
    motivation: str
    stress_score: float
    created_at: str

@router.post("", response_model=DumpOut)
async def create_dump(body: DumpIn, db: Session = Depends(get_db)):
    tags = ",".join(body.tags) if body.tags else None
    bundle = await generate_bundle(prompt=body.text, history_snippets=None)
    d = Dump(
        text=body.text,
        tags=tags,
        stress_score=bundle["stress_score"],
        action_plan=bundle["action_plan"],
        wellness_tip=bundle["wellness_tip"],
        motivation=bundle["motivation"],
    )
    db.add(d); db.commit(); db.refresh(d)
    return DumpOut(
        id=d.id,
        action_plan=d.action_plan,
        wellness_tip=d.wellness_tip,
        motivation=d.motivation,
        stress_score=d.stress_score,
        created_at=d.created_at.isoformat() if d.created_at else ""
    )

@router.get("", response_model=list[DumpOut])
def list_dumps(limit: int = 20, db: Session = Depends(get_db)):
    rows = db.query(Dump).order_by(Dump.id.desc()).limit(min(limit, 100)).all()
    return [
        DumpOut(
            id=r.id,
            action_plan=r.action_plan,
            wellness_tip=r.wellness_tip,
            motivation=r.motivation,
            stress_score=r.stress_score,
            created_at=r.created_at.isoformat() if r.created_at else ""
        ) for r in rows
    ]
