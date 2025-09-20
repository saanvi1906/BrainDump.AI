# 📜 AI Output Schema – Hackathon Demo

This schema defines the **exact JSON structure** that the AI must return.  
It ensures consistent outputs across backend, frontend, and testing.  

---

## 🎯 Fields

### `plan` (Array of Strings)
- **Definition**: 2–4 concrete, *doable* action steps.  
- **Format**: Each item ≤ 100 characters.  
- **Examples**:  
  - "Review class notes for 10 minutes"  
  - "Write 3 sentences for essay intro"  

---

### `reset_tip` (String)
- **Definition**: One short wellness action to reset.  
- **Format**: ≤ 80 characters.  
- **Examples**:  
  - "Stretch for 2 minutes"  
  - "Drink a glass of water"  

---

### `motivation` (String)
- **Definition**: 1–2 sentences of encouragement.  
- **Format**: ≤ 150 characters.  
- **Examples**:  
  - "You’ve already started—keep going, one step at a time!"  
  - "Small wins add up. You’ve got this 💪"  

---

### `stress_score` (Float)
- **Definition**: AI’s guess of stress intensity.  
- **Range**: 0.0 (calm) → 1.0 (max stressed).  
- **Examples**: 0.25, 0.78, 0.95  

---

## ✅ Example Output

```json
{
  "plan": [
    "List 3 key points for essay",
    "Draft one paragraph",
    "Review notes for 10 minutes"
  ],
  "reset_tip": "Stretch for 2 minutes",
  "motivation": "You are moving forward, even if it’s one small step 🚀",
  "stress_score": 0.72
}



---

## ✅ What to Do With It

1. **Put this file in your repo** as `SCHEMA.md`.  
   - This is the contract between backend, AI prompts, and frontend.  

2. **Backend (Divyanshu + you)**  
   - When you call the AI, **include this schema in the system prompt**.  
   - Example:  
     > “You are an assistant that converts stress notes into JSON following this schema: [paste schema]. Output strict JSON only.”  
   - After response, **check if all 4 keys exist**.  
   - If they don’t → re-prompt AI with a short “stick to schema” message.  

3. **Frontend (Saanvi)**  
   - Render each key according to the mapping section.  
   - Because the schema is fixed, she won’t have to guess data types.  

4. **Demo**  
   - This guarantees that every AI reply looks polished: tasks → reset → motivation → stress score.  
   - Judges see a structured output, not messy text.  

---

👉 Do you want me to also **write the exact Python snippet for re-prompting if schema breaks** so Divyanshu can copy-paste it into the backend? That way you won’t waste time debugging during the hackathon.
