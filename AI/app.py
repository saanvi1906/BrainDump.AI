# app.py
"""
BrainDump.AI FastAPI Backend
============================
Main FastAPI server that handles stress dumps and returns structured AI responses.

Flow:
1. User sends stress input via POST /dump
2. Server calls Ollama with PROMPT.md system prompt
3. Validates JSON response matches schema
4. Saves to Supermemory for future context
5. Returns structured response to frontend

Dependencies:
- fastapi: Web framework
- ollama: Local LLM client
- supermemory_client: Our custom wrapper for Supermemory API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os
from ollama import Client
from supermemory_client import save_entry, get_recent

# Initialize FastAPI app
app = FastAPI(
    title="BrainDump.AI",
    description="Transform student stress into actionable steps",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama client
ollama_client = Client()

# Load system prompt from PROMPT.md
def load_system_prompt():
    """Load the AI system prompt from PROMPT.md file"""
    try:
        with open("PROMPT.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="PROMPT.md file not found")

SYSTEM_PROMPT = load_system_prompt()

# Pydantic models for request/response validation
class StressDumpRequest(BaseModel):
    """Request model for stress dump input"""
    user_input: str = Field(..., min_length=1, max_length=1000, description="User's stress description")
    user_id: str = Field(..., min_length=1, max_length=100, description="Unique user identifier")
    tags: Optional[List[str]] = Field(default=[], description="Optional tags for categorization")

class StressDumpResponse(BaseModel):
    """Response model matching the JSON schema from PROMPT.md"""
    plan: List[str] = Field(..., description="2-4 actionable steps, max 100 chars each")
    reset_tip: str = Field(..., max_length=80, description="Short wellness tip")
    motivation: str = Field(..., max_length=150, description="Encouragement message")
    stress_score: float = Field(..., ge=0.0, le=1.0, description="Stress level from 0.0 to 1.0")

class RecentEntriesResponse(BaseModel):
    """Response model for recent entries"""
    entries: List[dict] = Field(..., description="List of recent stress dump entries")

def validate_ai_response(response_text: str) -> tuple[bool, str, dict]:
    """
    Validate AI response matches our JSON schema
    
    Args:
        response_text: Raw text response from Ollama
        
    Returns:
        (is_valid, error_message, parsed_data)
    """
    try:
        # Parse JSON
        data = json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", {}
    
    # Check required fields
    required_fields = ["plan", "reset_tip", "motivation", "stress_score"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {missing_fields}", data
    
    # Validate field types and constraints
    try:
        # Plan validation
        if not isinstance(data["plan"], list) or not (2 <= len(data["plan"]) <= 4):
            return False, "Plan must be a list of 2-4 steps", data
        
        for i, step in enumerate(data["plan"]):
            if not isinstance(step, str) or len(step) > 100:
                return False, f"Plan step {i+1} must be string ≤100 chars", data
        
        # Reset tip validation
        if not isinstance(data["reset_tip"], str) or len(data["reset_tip"]) > 80:
            return False, "Reset tip must be string ≤80 chars", data
        
        # Motivation validation
        if not isinstance(data["motivation"], str) or len(data["motivation"]) > 150:
            return False, "Motivation must be string ≤150 chars", data
        
        # Stress score validation
        if not isinstance(data["stress_score"], (int, float)) or not (0.0 <= data["stress_score"] <= 1.0):
            return False, "Stress score must be float between 0.0 and 1.0", data
        
        # Convert stress_score to float if it's an int
        data["stress_score"] = float(data["stress_score"])
        
        return True, "Valid response", data
        
    except Exception as e:
        return False, f"Validation error: {str(e)}", data

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "BrainDump.AI API is running!", "status": "healthy"}

@app.post("/dump", response_model=StressDumpResponse)
async def process_stress_dump(request: StressDumpRequest):
    """
    Main endpoint: Process stress dump and return structured AI response
    
    Flow:
    1. Get recent entries for context (optional)
    2. Call Ollama with system prompt + user input
    3. Validate JSON response
    4. Save to Supermemory
    5. Return structured response
    """
    try:
        # Get recent entries for context (optional enhancement)
        recent_entries = get_recent(request.user_id, limit=3)
        
        # Prepare context from recent entries
        context = ""
        if recent_entries:
            context = "\n\nRecent patterns:\n"
            for entry in recent_entries[:2]:  # Use only last 2 for context
                if hasattr(entry, 'content'):
                    context += f"- {entry.content[:100]}...\n"
        
        # Call Ollama with system prompt
        response = ollama_client.chat(
            model="llama2",  # Configure model as needed
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.user_input + context}
            ]
        )
        
        ai_response_text = response['message']['content']
        
        # Validate response
        is_valid, error_msg, parsed_data = validate_ai_response(ai_response_text)
        
        # If invalid, try re-prompting once
        if not is_valid:
            re_prompt_text = "Return JSON strictly as per schema: plan, reset_tip, motivation, stress_score."
            response = ollama_client.chat(
                model="llama2",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": request.user_input + "\n" + re_prompt_text}
                ]
            )
            ai_response_text = response['message']['content']
            is_valid, error_msg, parsed_data = validate_ai_response(ai_response_text)
        
        # If still invalid, return error
        if not is_valid:
            raise HTTPException(
                status_code=500, 
                detail=f"AI response validation failed: {error_msg}"
            )
        
        # Save to Supermemory
        try:
            save_entry(
                user_id=request.user_id,
                user_input=request.user_input,
                ai_output=parsed_data,
                tags=request.tags
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Warning: Failed to save to Supermemory: {e}")
        
        # Return structured response
        return StressDumpResponse(**parsed_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/recent/{user_id}", response_model=RecentEntriesResponse)
async def get_user_recent_entries(user_id: str, limit: int = 5):
    """
    Get recent stress dump entries for a user
    
    Args:
        user_id: User identifier
        limit: Maximum number of entries to return (default: 5)
    """
    try:
        entries = get_recent(user_id, limit=limit)
        return RecentEntriesResponse(entries=entries)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve entries: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check including dependencies"""
    health_status = {
        "status": "healthy",
        "timestamp": "2024-01-20T10:00:00Z",  # You can use datetime.now().isoformat()
        "dependencies": {
            "ollama": "connected",  # You can add actual checks here
            "supermemory": "connected"
        }
    }
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)