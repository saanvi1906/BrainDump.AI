from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    text: str
    plan: str
    reset: str
    motivation: str
    score: float
    color: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Dump(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    text: str
    tags: Optional[str] = None
    action_plan: str
    wellness_tip: str
    motivation: str
    stress_score: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
