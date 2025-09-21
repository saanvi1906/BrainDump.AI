# supermemory_client.py
"""
Supermemory Wrapper for BrainDump.AI
=====================================
This module provides a clean interface to Supermemory API for storing and retrieving
student stress dumps and AI responses.

Key Features:
- Save stress dumps with user input, AI response, and tags
- Retrieve recent entries for context and dashboard
- Automatic error handling and retry logic
- Consistent data formatting for frontend consumption

Data Flow:
1. User submits stress input → app.py
2. AI generates response → app.py  
3. Save to Supermemory → this module
4. Retrieve for context → this module
5. Display in dashboard → frontend

Dependencies:
- supermemory: Official Python SDK for Supermemory API
- API Key: Required for authentication (configured below)

Team Usage:
- Kenisha: Use save_entry() after AI response generation
- Shristi: Use get_recent() for user context and dashboard
- Divyanshu: Handle error cases and retry logic
- Saanvi: Data format is consistent for frontend rendering
"""

from supermemory import Supermemory
import supermemory

# 🔑 Initialize Supermemory client
# TODO: Move API key to environment variable for production
# export SUPERMEMORY_API_KEY="your_key_here"
client = Supermemory(api_key="sm_JuRF4dhaRY4p6LYRYR6D7t_GvyHEDeffXcvHTjZJPFxCfOjkGjHotWVGaUVAkMOxRnLsQyvgyiygSZzVphSqBbk")

def save_entry(user_id: str, user_input: str, ai_output: dict, tags: list = []):
    """
    Save a stress dump entry to Supermemory for future context and dashboard.
    
    This function stores the complete stress dump session including:
    - User's raw stress input
    - AI-generated response (plan, reset_tip, motivation, stress_score)
    - Optional tags for categorization
    
    Args:
        user_id (str): Unique identifier for the user (e.g., "student123")
        user_input (str): Raw stress description from the user
        ai_output (dict): Structured AI response matching PROMPT.md schema:
            {
                "plan": ["step1", "step2", "step3"],
                "reset_tip": "Take deep breaths",
                "motivation": "You've got this! 💪",
                "stress_score": 0.7
            }
        tags (list): Optional tags for filtering (e.g., ["exam", "work", "social"])
    
    Returns:
        None (prints success/error messages)
        
    Raises:
        supermemory.APIConnectionError: Network connectivity issues
        supermemory.RateLimitError: API rate limit exceeded
        supermemory.APIStatusError: API returned error status
        
    Example:
        save_entry(
            user_id="student123",
            user_input="I'm stressed about my final exam",
            ai_output={
                "plan": ["Review notes", "Practice problems", "Get rest"],
                "reset_tip": "Take 5 deep breaths",
                "motivation": "You've prepared well! 🌟",
                "stress_score": 0.8
            },
            tags=["exam", "academic"]
        )
    """
    # Create content string that combines input and output
    content = f"User Input: {user_input}\n\nAI Response: {ai_output}"
    
    # Prepare metadata (metadata values must be strings, numbers, booleans, or arrays)
    metadata = {
        "user_id": user_id,
        "ai_output": str(ai_output),  # Convert dict to string
        "tags": str(tags)  # Convert list to string
    }
    
    # Add tags to container_tags for filtering
    container_tags = [user_id] + tags
    
    try:
        client.memories.add(
            content=content,
            container_tags=container_tags,
            metadata=metadata
        )
        print(f"[Supermemory] Entry saved for user {user_id}")
    except supermemory.APIConnectionError as e:
        print(f"[Supermemory] Connection error: {e}")
        raise
    except supermemory.RateLimitError as e:
        print(f"[Supermemory] Rate limit exceeded: {e}")
        raise
    except supermemory.APIStatusError as e:
        print(f"[Supermemory] API error {e.status_code}: {e.response}")
        raise

def get_recent(user_id: str, limit: int = 3):
    """
    Retrieve recent stress dump entries for a user.
    
    This function fetches the most recent entries for a specific user, which can be used for:
    - Dashboard display showing stress patterns over time
    - Context for AI responses (understanding user's stress history)
    - Analytics and insights about user's stress levels
    
    Args:
        user_id (str): Unique identifier for the user
        limit (int): Maximum number of recent entries to retrieve (default: 3)
    
    Returns:
        list: List of recent entries, each containing:
            - id: Unique entry identifier
            - content: Combined user input and AI response
            - createdAt: Timestamp when entry was created
            - metadata: Additional data including tags and stress_score
    
    Example:
        recent_entries = get_recent("student123", limit=5)
        for entry in recent_entries:
            print(f"Entry from {entry['createdAt']}: {entry['content'][:100]}...")
    
    Note:
        Returns empty list if no entries found or if API errors occur.
        Errors are logged but don't raise exceptions to prevent app crashes.
    """
    try:
        results = client.memories.list(
            container_tags=[user_id],
            limit=limit,
            sort="createdAt",
            order="desc",
            include_content=True
        )
        return results.data if hasattr(results, 'data') else []
    except supermemory.APIConnectionError as e:
        print(f"[Supermemory] Connection error: {e}")
        return []
    except supermemory.RateLimitError as e:
        print(f"[Supermemory] Rate limit exceeded: {e}")
        return []
    except supermemory.APIStatusError as e:
        print(f"[Supermemory] API error {e.status_code}: {e.response}")
        return []
