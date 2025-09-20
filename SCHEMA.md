# 🌟 BrainDump – AI Output Schema (Commented Version)

# --------------------------
# OVERVIEW
# --------------------------
# This file defines the AI JSON output format for BrainDump.
# All teammates should refer to this file to know what fields
# exist, how they are formatted, and who owns which tasks.
# Backend validation, frontend rendering, and AI prompting
# all depend on this schema.

# --------------------------
# JSON SCHEMA (AI Output)
# --------------------------
# plan: array of short strings (2-4 actionable tasks)
# reset_tip: short wellness action (1 sentence)
# motivation: short encouragement (1-2 sentences)
# stress_score: float 0.0–1.0 representing stress intensity

{
  "plan": ["string", "string", "string"],      # 2–4 items; Kenisha maps to dashboard; Saanvi renders as card 1
  "reset_tip": "string",                       # short wellness tip; Saanvi renders as card 2
  "motivation": "string",                      # short encouragement; Saanvi renders as card 3
  "stress_score": 0.0                          # 0–1 float; Kenisha converts to color blob for dashboard
}

# --------------------------
# FIELD DEFINITIONS
# --------------------------
# plan: actionable steps like "Review notes for 10 min"
# reset_tip: wellness action like "Drink a glass of water"
# motivation: encouragement like "You’ve got this!"
# stress_score: 0.0 calm → 1.0 very stressed

# --------------------------
# TEAM ROLES
# --------------------------
# Kenisha:
#   - Maintain schema file
#   - Validate AI outputs
#   - Map stress_score to color blobs on dashboard
# Shristi:
#   - Use schema in AI prompts
#   - Tune AI to reliably output JSON
#   - Connect voice input → text → schema-compliant JSON
# Divyanshu:
#   - Backend: call AI with schema
#   - Validate + re-prompt if schema is broken
#   - Store outputs in DB
# Saanvi:
#   - Frontend: render fields as cards/dashboard
#   - Build animations around these fixed fields

# --------------------------
# EXAMPLE INPUT → OUTPUT
# --------------------------
# Input:
# "I have 3 exams next week and I haven’t started studying. I feel overwhelmed."
#
# AI Output (JSON):
{
  "plan": [
    "Make a list of exam topics",
    "Study for 25 minutes on subject 1",
    "Take a 5 minute stretch break"
  ],
  "reset_tip": "Drink a glass of water before starting",
  "motivation": "You’ve done this before and passed. One step at a time gets you there.",
  "stress_score": 0.82
}

# --------------------------
# BACKEND PYTHON SNIPPET (Divyanshu)
# --------------------------
# This shows how to call the AI, validate JSON, and re-prompt if invalid
#
# import json
# from openai import OpenAI
# client = OpenAI()
#
# schema_text = """[PASTE SCHEMA BLOCK HERE]"""
#
# def call_ai_with_schema(user_input):
#     # First attempt
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": schema_text},
#             {"role": "user", "content": user_input}
#         ],
#     )
#     text = response.choices[0].message.content
#     try:
#         data = json.loads(text)
#         if all(k in data for k in ["plan", "reset_tip", "motivation", "stress_score"]):
#             return data
#         else:
#             raise ValueError("Missing keys")
#     except Exception:
#         # Re-prompt if invalid
#         fix_response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": schema_text},
#                 {"role": "user", "content": f"Stick to the JSON schema only. Input: {user_input}"}
#             ],
#         )
#         return json.loads(fix_response.choices[0].message.content)
#
# Example usage:
# output = call_ai_with_schema("I have too many assignments and no time.")
# print(json.dumps(output, indent=2))

# --------------------------
# NOTES
# --------------------------
# - Use this as the single source of truth for the hackathon.
# - Always copy schema into AI prompts.
# - Backend validation + re-prompt ensures demo reliability.
# - Frontend renders fixed fields → clean UI, no guessing.
# - Emojis optional in motivation for demo flair.

