from supermemory_client import save_entry, get_recent

# Example: save a new dump
save_entry(
    user_id="kenisha123",
    user_input="I'm stressed about my exam tomorrow",
    ai_output={
        "plan": ["Review key notes", "Do 2 practice problems"],
        "reset_tip": "Take a 5 min walk",
        "motivation": "You’ve got this 💪 Just focus one step at a time.",
        "stress_score": 0.7
    },
    tags=["exam"]
)

# Example: fetch last 3 entries
recent = get_recent("kenisha123", limit=3)
print(recent)
