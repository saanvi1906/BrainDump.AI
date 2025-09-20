# BrainDump.AI: AI Stress to Success Hub

**Turn student stress into clarity, actionable steps, and emotional support — instantly.**

---

## What is BrainDump.AI?
Students face constant pressure from exams, deadlines, internships, and life. BrainDump.AI is an AI-powered web app that transforms messy stress dumps (typed or spoken) into three immediate, useful outputs:

- **Action Plan** — 2–4 tiny, doable steps you can start right now.  
- **Wellness Reset Tip** — a one-line micro-reset (stretch, hydrate, breathe).  
- **Motivation Boost** — a short encouraging reframe to build confidence.  
- **Stress Score** — a 0.0–1.0 metric that feeds the Mood Dashboard.

BrainDump.AI bridges the gap between journaling, productivity, and wellness — giving students clarity and momentum, not just stored notes.

---

## Key Features (Hackathon MVP)
- **Stress Dump → Magic Reveal**: type or speak your worry and watch it turn into three clean cards (Plan, Reset, Motivation).  
- **Mood Dashboard**: color-coded stress blobs over time (green → calm, red → stressed) to visualize progress.  
- **Voice-to-Plan**: optional speech input converts to text then to structured output.  
- **Supermemory Integration**: stores context and previous dumps so the AI can provide trend-aware insights (e.g., “You’ve been stressed about deadlines 3 days in a row — try scheduling early breaks”).  
- **Polish-ready UI**: short, frontend-friendly outputs guaranteed by the prompt + schema.

---

## How It Works (10-Second Demo)
1. User: "I'm drowning in assignments and don't know where to start."  
2. BrainDump.AI returns:
   - **Plan**: `["List 3 urgent tasks", "Set a 25-min timer", "Finish one task"]`  
   - **Reset Tip**: `"Stand and stretch for 2 minutes"`  
   - **Motivation**: `"One step at a time — you've got this! 💪"`  
   - **Stress Score**: `0.83` (renders as a red blob)  
3. With **Supermemory**, the AI remembers patterns across dumps and suggests better strategies over time.  
4. Over days, stress blobs move toward green — visible progress.

---

## How Supermemory is Used
Supermemory powers the *continuity* of BrainDump.AI:

- Each stress dump (input + AI output) is stored in Supermemory.  
- When a new dump arrives, BrainDump.AI fetches relevant past entries (last few days or recurring themes).  
- The LLM uses this context to give more **personalized advice**:  
  - Instead of just reacting to today’s input, it connects trends (e.g., “This is your 4th late-night stress entry this week. Consider an earlier study block tomorrow.”).  
- The **Mood Dashboard** visualizes these Supermemory logs into stress trend blobs.  

👉 Without Supermemory: one-off, isolated tips.  
👉 With Supermemory: evolving, context-aware guidance.

---

## Why It Wins
- **Instant, demo-ready transformation** — perfect for judges: chaos → clarity in seconds.  
- **Holistic**: combines practical task guidance with emotional care.  
- **Memory-driven insights**: via **Supermemory**, BrainDump.AI isn’t just reactive — it learns from past entries.  
- **Scalable**: works with Ollama, OpenAI, and Supermemory backends.  
- **Sticky UX**: memory + dashboard make the product valuable over time.

---

## Vision
BrainDump.AI aims to become a trusted student wellness companion: proactive nudges, contextual help, and a habit-forming dashboard that turns short-term relief into long-term resilience.

---

## License & Notes
This repo contains hackathon materials (prompt, test scripts, demo assets).  
- `PROMPT.md` defines the system prompt and JSON schema.  
- `SCHEMA.md` explains output formatting for backend/frontend integration.  
- **Supermemory** provides continuity across sessions, enabling smarter, personalized suggestions.  

---
