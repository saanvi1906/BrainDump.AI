import json
from openai import OpenAI

client = OpenAI()

# Load schema for system prompt
schema_text = """
You are an assistant that converts student stress notes into JSON.
Follow this schema strictly:

{
  "plan": ["string", "string", "string"],
  "reset_tip": "string",
  "motivation": "string",
  "stress_score": 0.0
}

Rules:
- Always output JSON only (no explanations, no text outside JSON).
- plan: 2-4 short actionable steps.
- reset_tip: one short wellness action.
- motivation: short encouragement (1-2 sentences).
- stress_score: float between 0.0 and 1.0.
"""

def call_ai_with_schema(user_input):
    # First attempt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": schema_text},
            {"role": "user", "content": user_input}
        ],
    )

    text = response.choices[0].message.content

    try:
        data = json.loads(text)
        if all(k in data for k in ["plan", "reset_tip", "motivation", "stress_score"]):
            return data
        else:
            raise ValueError("Missing keys")
    except Exception:
        # If schema fails, re-prompt AI
        fix_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": schema_text},
                {"role": "user", "content": f"Stick to the JSON schema only. Input: {user_input}"}
            ],
        )
        return json.loads(fix_response.choices[0].message.content)

# Example usage
if __name__ == "__main__":
    user_input = "I have too many assignments and no time."
    output = call_ai_with_schema(user_input)
    print(json.dumps(output, indent=2))

---

✅ Copy this whole thing into `SCHEMA.md` in your repo.  
- You own keeping it updated.  
- Divyanshu literally copies the Python snippet into `/transform`.  
- Shristi copies the schema block into her prompt tests.  
- Saanvi uses the mapping section to build UI cards.  
