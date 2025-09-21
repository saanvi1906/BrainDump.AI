# BrainDump.AI Backend Setup Guide

## 🎯 Overview

BrainDump.AI transforms student stress into actionable steps using AI. This backend provides:
- ✅ Step-by-step action plans
- 💆 Wellness reset tips  
- 💡 Motivation boosts
- 📊 Stress score tracking

## 🏗️ Architecture

```
User Input → FastAPI → Ollama (LLM) → JSON Response → Supermemory → Dashboard
```

## 📁 File Structure

```
backend/
├── app.py                    # FastAPI server (main backend)
├── supermemory_client.py     # Supermemory API wrapper
├── test_prompt_ollama.py     # Test script for PROMPT.md
├── PROMPT.md                 # AI system prompt & JSON schema
├── requirements.txt          # Python dependencies
└── prompt_test_results.csv   # Test results (generated)
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Ollama (Local LLM)
```bash
# Install Ollama first: https://ollama.ai
ollama pull llama2
ollama serve
```

### 3. Test the System
```bash
# Test PROMPT.md with Ollama
python3 test_prompt_ollama.py

# Start FastAPI server
python3 app.py
```

### 4. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/

# Process stress dump
curl -X POST "http://localhost:8000/dump" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I am stressed about my exam",
    "user_id": "student123",
    "tags": ["exam"]
  }'
```

## 📋 API Endpoints

### POST `/dump`
Process a stress dump and return structured AI response.

**Request:**
```json
{
  "user_input": "I'm overwhelmed with homework",
  "user_id": "student123", 
  "tags": ["academic", "homework"]
}
```

**Response:**
```json
{
  "plan": ["Break into smaller tasks", "Set 25-min timer", "Take breaks"],
  "reset_tip": "Take 5 deep breaths",
  "motivation": "You've got this! 💪",
  "stress_score": 0.7
}
```

### GET `/recent/{user_id}`
Get recent stress dump entries for dashboard.

### GET `/health`
Health check endpoint.

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Move API key to environment
export SUPERMEMORY_API_KEY="your_key_here"
```

### Model Configuration
Edit `app.py` to change the Ollama model:
```python
model="llama2"  # Change to your preferred model
```

## 🧪 Testing

### Test PROMPT.md
```bash
python3 test_prompt_ollama.py
```
This validates the AI prompt against multiple stress scenarios and saves results to CSV.

### Test Integration
```bash
python3 -c "from supermemory_client import save_entry, get_recent; print('✅ Integration works')"
```

## 📊 JSON Schema

All AI responses follow this strict schema:

```json
{
  "plan": ["step1", "step2", "step3"],     // 2-4 steps, ≤100 chars each
  "reset_tip": "Take deep breaths",         // ≤80 chars
  "motivation": "You've got this! 💪",      // ≤150 chars  
  "stress_score": 0.7                       // 0.0-1.0 float
}
```

## 👥 Team Usage

- **Kenisha**: Configure FastAPI endpoints and JSON validation
- **Shristi**: Adjust PROMPT.md for different stress scenarios
- **Divyanshu**: Handle Supermemory integration and error cases
- **Saanvi**: Use consistent JSON schema for frontend rendering

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not responding**
   ```bash
   ollama serve  # Start Ollama server
   ollama list   # Check available models
   ```

2. **Supermemory API errors**
   - Check API key in `supermemory_client.py`
   - Verify internet connection
   - Check API rate limits

3. **JSON validation failures**
   - Run `test_prompt_ollama.py` to debug
   - Check PROMPT.md examples
   - Verify model is following instructions

### Debug Mode
Add debug logging to `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Production Deployment

1. **Environment Variables**
   ```bash
   export SUPERMEMORY_API_KEY="prod_key"
   export OLLAMA_MODEL="llama2"
   ```

2. **Production Server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Frontend Integration**
   - CORS is enabled for all origins
   - API returns consistent JSON schema
   - Error handling prevents crashes

## 📈 Next Steps

- [ ] Add user authentication
- [ ] Implement rate limiting
- [ ] Add analytics dashboard
- [ ] Optimize for mobile frontend
- [ ] Add more AI models support

---

**Ready for hackathon! 🎉** All files are consistent, well-documented, and tested.
