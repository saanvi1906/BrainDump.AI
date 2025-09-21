import os
import json
import ast
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field as PField
from sqlmodel import SQLModel, Field, Session, create_engine, select
from dotenv import load_dotenv
import httpx
from utils.scoring import score_to_color

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./braindump.db")
engine = create_engine(DATABASE_URL, echo=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class TransformRequest(BaseModel):
    user_id: str
    text: str

class EntryOut(BaseModel):
    id: int
    user_id: str
    text: str
    plan: List[str]
    reset: str
    motivation: str
    score: float = PField(ge=0.0, le=1.0)
    color: str
    created_at: datetime

class EntriesResponse(BaseModel):
    entries: List[EntryOut]

SQLModel.metadata.create_all(engine)

SYSTEM_PROMPT = (
    "You are BrainDump. Return strict JSON with keys plan, reset, motivation, score. "
    "plan: 2-4 micro-steps, imperative. reset: 1 actionable tip. motivation: 1 sentence. "
    "score: float in [0,1]. No extra text."
)

async def ollama_json_chat(user_text: str) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        payload = {
            "model": "llama3.1:8b",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            "options": {"temperature": 0.6},
            "stream": False,
            "format": "json"
        }
        r = await client.post("http://127.0.0.1:11434/api/chat", json=payload)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Ollama error {r.status_code}: {r.text}")
        content = r.json().get("message", {}).get("content", "").strip()
        try:
            return json.loads(content)
        except Exception:
            raise HTTPException(status_code=502, detail="Bad JSON from model")

def coerce_plan_list(x) -> List[str]:
    if isinstance(x, list):
        return [str(i).strip() for i in x if str(i).strip()]
    if isinstance(x, str):
        s = x.strip()
        try:
            v = json.loads(s)
            if isinstance(v, list):
                return [str(i).strip() for i in v if str(i).strip()]
        except Exception:
            try:
                v = ast.literal_eval(s)
                if isinstance(v, list):
                    return [str(i).strip() for i in v if str(i).strip()]
            except Exception:
                pass
        parts = [p.strip(" -•\t") for p in s.split("\n") if p.strip()]
        return parts if parts else [s]
    return [str(x)]

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/transform", response_model=EntryOut)
async def transform(payload: TransformRequest):
    data = await ollama_json_chat(payload.text)
    for k in ["plan", "reset", "motivation", "score"]:
        if k not in data:
            raise HTTPException(status_code=502, detail="Missing keys in model output")
    try:
        score = float(data["score"])
        if score < 0 or score > 1:
            raise ValueError("out of range")
    except Exception:
        raise HTTPException(status_code=502, detail="Invalid score")
    plan_list = coerce_plan_list(data["plan"])
    color = score_to_color(score)
    entry = Entry(
        user_id=payload.user_id,
        text=payload.text,
        plan=json.dumps(plan_list),
        reset=str(data["reset"]),
        motivation=str(data["motivation"]),
        score=score,
        color=color
    )
    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return EntryOut(
            id=entry.id,
            user_id=entry.user_id,
            text=entry.text,
            plan=plan_list,
            reset=entry.reset,
            motivation=entry.motivation,
            score=entry.score,
            color=entry.color,
            created_at=entry.created_at
        )

@app.get("/entries", response_model=EntriesResponse)
def entries(user_id: str = Query(...)):
    with Session(engine) as session:
        stmt = select(Entry).where(Entry.user_id == user_id).order_by(Entry.created_at.desc())
        rows = session.exec(stmt).all()
        out = []
        for e in rows:
            plan_list = coerce_plan_list(e.plan)
            out.append(
                EntryOut(
                    id=e.id,
                    user_id=e.user_id,
                    text=e.text,
                    plan=plan_list,
                    reset=e.reset,
                    motivation=e.motivation,
                    score=e.score,
                    color=e.color,
                    created_at=e.created_at
                )
            )
        return EntriesResponse(entries=out)
