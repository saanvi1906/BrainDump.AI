from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime

app = FastAPI(
    title="BrainDump.AI",
    description="Transform student stress into actionable steps",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
dumps_storage = []

# Pydantic models
class StressDumpRequest(BaseModel):
    user_input: str
    user_id: str
    tags: Optional[List[str]] = []

class StressDumpResponse(BaseModel):
    plan: List[str]
    reset_tip: str
    motivation: str
    stress_score: float

class RecentEntriesResponse(BaseModel):
    entries: List[dict]

# Simple AI processing (without external dependencies)
def process_stress_dump(user_input: str) -> StressDumpResponse:
    """Simple stress processing without external AI"""
    
    # Simple stress scoring based on keywords
    stress_keywords = ["stressed", "anxious", "worried", "overwhelmed", "panic", "deadline", "exam"]
    stress_score = min(1.0, sum(1 for word in stress_keywords if word.lower() in user_input.lower()) * 0.2)
    
    # Generate simple responses based on input
    if "exam" in user_input.lower() or "test" in user_input.lower():
        plan = [
            "Break your study material into 3 manageable chunks",
            "Set a 25-minute timer and focus on one chunk",
            "Take a 5-minute break, then repeat",
            "Review what you learned for 10 minutes"
        ]
        reset_tip = "Take 5 deep breaths and drink some water. You've got this!"
        motivation = "Every expert was once a beginner. You're learning and growing every day."
    elif "deadline" in user_input.lower():
        plan = [
            "List all tasks that need to be done",
            "Prioritize by importance and urgency",
            "Start with the most critical task",
            "Ask for help if you need it"
        ]
        reset_tip = "Stand up, stretch your arms, and take 3 deep breaths."
        motivation = "You've handled deadlines before and succeeded. This one is no different."
    else:
        plan = [
            "Write down everything that's bothering you",
            "Choose one small thing you can do right now",
            "Do that one thing",
            "Celebrate the small win"
        ]
        reset_tip = "Take a walk around the room and drink some water."
        motivation = "You're stronger than you think. Take it one step at a time."
    
    return StressDumpResponse(
        plan=plan,
        reset_tip=reset_tip,
        motivation=motivation,
        stress_score=stress_score
    )

# Routes
@app.get("/")
async def root():
    return {"message": "BrainDump.AI API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "ollama": "not_required",
            "supermemory": "not_required"
        }
    }

@app.post("/dump", response_model=StressDumpResponse)
async def process_stress_dump_endpoint(request: StressDumpRequest):
    """Process stress dump and return structured AI response"""
    
    # Process the stress dump
    response = process_stress_dump(request.user_input)
    
    # Store the dump
    dump_entry = {
        "user_id": request.user_id,
        "user_input": request.user_input,
        "tags": request.tags,
        "response": response.dict(),
        "timestamp": datetime.now().isoformat()
    }
    dumps_storage.append(dump_entry)
    
    return response

@app.get("/recent/{user_id}", response_model=RecentEntriesResponse)
async def get_user_recent_entries(user_id: str, limit: int = 5):
    """Get recent stress dump entries for a user"""
    
    user_entries = [
        entry for entry in dumps_storage 
        if entry["user_id"] == user_id
    ]
    
    # Sort by timestamp (most recent first) and limit
    user_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_entries = user_entries[:limit]
    
    return RecentEntriesResponse(entries=recent_entries)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

