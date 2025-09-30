import os
import httpx
from config import settings

SM_API = "https://api.supermemory.ai"
SM_KEY = settings.SUPERMEMORY_API_KEY

def _headers():
    return {"Authorization": f"Bearer {SM_KEY}", "Content-Type": "application/json"}

async def add_memory(user_id: str, text: str, plan: list[str], score: float, color: str, tags: list[str] | None = None):
    if not SM_KEY:
        return None
    content = f"user_id: {user_id}\ntext: {text}\nplan: " + "; ".join(plan) + f"\nscore: {score}\ncolor: {color}"
    payload = {
        "content": content,
        "userId": user_id,
        "containerTags": [f"user:{user_id}", "braindump"] + (tags or [])
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{SM_API}/v3/documents", headers=_headers(), json=payload)
        r.raise_for_status()
        return r.json()

async def search_memories(user_id: str, query: str, limit: int = 3, threshold: float = 0.6):
    if not SM_KEY:
        return {"results": []}
    payload = {
        "q": query,
        "containerTag": f"user:{user_id}",
        "threshold": threshold,
        "limit": limit
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{SM_API}/v4/search", headers=_headers(), json=payload)
        r.raise_for_status()
        return r.json()

async def recent_memories(user_id: str, limit: int = 5):
    return await search_memories(user_id, "*", limit=limit, threshold=0.0)
