# supermemory_client.py
"""
Supermemory Wrapper for BrainDump.AI
------------------------------------
This file provides simple helper functions for:
1. Saving new entries into Supermemory (input + output + tags).
2. Retrieving recent entries for a given user.

Dependencies:
- supermemory (Python SDK or API client)
"""

from supermemory import Supermemory  # make sure you've installed the supermemory package
import supermemory

# 🔑 Initialize the client
client = Supermemory(api_key="sm_JuRF4dhaRY4p6LYRYR6D7t_GvyHEDeffXcvHTjZJPFxCfOjkGjHotWVGaUVAkMOxRnLsQyvgyiygSZzVphSqBbk")

def save_entry(user_id: str, user_input: str, ai_output: dict, tags: list = []):
    """
    Save a stress dump entry into Supermemory.

    Args:
        user_id (str): Unique ID of the user
        user_input (str): Raw stress text from the user
        ai_output (dict): JSON response from Ollama (plan, reset_tip, motivation, stress_score)
        tags (list): Optional tags for categorization (e.g., ["exam", "project"])
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
    Retrieve recent entries for context.

    Args:
        user_id (str): Unique ID of the user
        limit (int): Number of past entries to fetch (default: 3)

    Returns:
        list: Recent entries (list of dicts)
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
