import os
import json
import ast
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field as PField
from sqlmodel import Session, select, SQLModel
from dotenv import load_dotenv
import httpx
from config import settings
from database import engine, init_db
from models import Entry, Dump
from utils.scoring import score_to_color
from utils.supermemory_client import search_memories, add_memory, recent_memories

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_CORS_ORIGINS == "*" else [o.strip() for o in settings.APP_CORS_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _load_prompt() -> str:
    p = os.path.join("prompts", "PROMPT.md")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Return JSON with keys plan, reset, motivation, score."

SYSTEM_PROMPT = _load_prompt()

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

class DumpCreate(BaseModel):
    user_id: str
    text: str
    tags: Optional[List[str]] = None

class DumpOut(BaseModel):
    id: int
    user_id: str
    text: str
    tags: Optional[List[str]] = None
    action_plan: str
    wellness_tip: str
    motivation: str
    stress_score: float
    created_at: datetime

class DumpsResponse(BaseModel):
    dumps: List[DumpOut]

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

async def build_context(user_id: str, query: str) -> str:
    try:
        res = await search_memories(user_id, query, limit=3, threshold=0.6)
        items = [m.get("memory", "")[:300] for m in res.get("results", []) if m.get("memory")]
        joined = "\n".join(items[:3]).strip()
        if not joined:
            return ""
        ctx = "Relevant past notes and preferences:\n" + joined
        return ctx[:1000]
    except Exception:
        return ""

async def ollama_json_chat(messages: list[dict]) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        payload = {
            "model": settings.LLM_MODEL,
            "messages": messages,
            "options": {"temperature": 0.6, "num_ctx": 1024},
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

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True, "model": settings.LLM_MODEL}

@app.post("/transform", response_model=EntryOut)
async def transform(payload: TransformRequest):
    ctx = await build_context(payload.user_id, payload.text)
    sys = SYSTEM_PROMPT if not ctx else SYSTEM_PROMPT + "\n" + ctx
    messages = [
        {"role": "system", "content": sys},
        {"role": "user", "content": payload.text}
    ]
    data = await ollama_json_chat(messages)
    if "plan" not in data and "action_plan" in data:
        data["plan"] = data["action_plan"]
    if "reset" not in data and "reset_tip" in data:
        data["reset"] = data["reset_tip"]
    if "score" not in data and "stress_score" in data:
        data["score"] = data["stress_score"]
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
    with Session(engine) as session:
        entry = Entry(
            user_id=payload.user_id,
            text=payload.text,
            plan=json.dumps(plan_list),
            reset=str(data["reset"]),
            motivation=str(data["motivation"]),
            score=score,
            color=color
        )
        session.add(entry)
        session.commit()
        session.refresh(entry)
        out = EntryOut(
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
    try:
        await add_memory(payload.user_id, payload.text, plan_list, score, color, tags=None)
    except Exception:
        pass
    return out

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

@app.post("/dump", response_model=DumpOut)
async def dump_create(body: DumpCreate):
    tr = TransformRequest(user_id=body.user_id, text=body.text)
    res = await transform(tr)
    action_plan = "\n".join(res.plan)
    wellness_tip = res.reset
    motivation = res.motivation
    stress_score = res.score
    with Session(engine) as session:
        d = Dump(
            user_id=body.user_id,
            text=body.text,
            tags=",".join(body.tags) if body.tags else None,
            action_plan=action_plan,
            wellness_tip=wellness_tip,
            motivation=motivation,
            stress_score=stress_score
        )
        session.add(d)
        session.commit()
        session.refresh(d)
        return DumpOut(
            id=d.id,
            user_id=d.user_id,
            text=d.text,
            tags=(d.tags.split(",") if d.tags else None),
            action_plan=d.action_plan,
            wellness_tip=d.wellness_tip,
            motivation=d.motivation,
            stress_score=d.stress_score,
            created_at=d.created_at
        )

@app.get("/dumps", response_model=DumpsResponse)
def dumps_list(user_id: Optional[str] = None, limit: int = 20):
    with Session(engine) as session:
        stmt = select(Dump)
        if user_id:
            stmt = stmt.where(Dump.user_id == user_id)
        stmt = stmt.order_by(Dump.created_at.desc()).limit(limit)
        rows = session.exec(stmt).all()
        out = []
        for d in rows:
            out.append(
                DumpOut(
                    id=d.id,
                    user_id=d.user_id,
                    text=d.text,
                    tags=(d.tags.split(",") if d.tags else None),
                    action_plan=d.action_plan,
                    wellness_tip=d.wellness_tip,
                    motivation=d.motivation,
                    stress_score=d.stress_score,
                    created_at=d.created_at
                )
            )
        return DumpsResponse(dumps=out)

@app.get("/recent/{user_id}")
async def recent(user_id: str, limit: int = 5):
    res = await recent_memories(user_id, limit=limit)
    return res
