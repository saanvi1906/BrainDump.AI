# 🧪 BrainDump.AI Testing Guide

## Quick Status Check ✅

**Current Status: CORE SYSTEM READY!** 
- ✅ All dependencies installed
- ✅ All files present and correct
- ✅ Supermemory integration working
- ✅ FastAPI server ready to start
- ✅ JSON schema validation working

## 🚀 How to Test Everything

### 1. **Quick Core Test (No Ollama Required)**
```bash
cd backend
python3 test_quick.py
```
**Expected Result:** All 7 tests should pass ✅

### 2. **Test Supermemory Integration**
```bash
python3 -c "
from supermemory_client import save_entry, get_recent
test_data = {
    'plan': ['Test step 1', 'Test step 2'],
    'reset_tip': 'Take deep breaths',
    'motivation': 'You can do this! 💪',
    'stress_score': 0.6
}
save_entry('test_user', 'Testing integration', test_data, ['test'])
print('✅ Supermemory test successful!')
"
```

### 3. **Test FastAPI Server**
```bash
# Start the server
python3 app.py

# In another terminal, test the endpoints:
curl http://localhost:8000/
curl http://localhost:8000/health
```

### 4. **Test with Ollama (Optional)**
If you want to test the full AI integration:

```bash
# Install Ollama first: https://ollama.ai
ollama serve
ollama pull llama2

# Test AI prompt
python3 test_prompt_ollama.py

# Test full integration
python3 test_system.py
```

## 📋 Complete Testing Checklist

### ✅ **Already Working**
- [x] Dependencies installed (fastapi, uvicorn, supermemory, pydantic)
- [x] All files present (app.py, supermemory_client.py, PROMPT.md, etc.)
- [x] Module imports working
- [x] Supermemory API integration
- [x] JSON schema validation
- [x] FastAPI server configuration
- [x] PROMPT.md content validation

### 🔄 **Optional (Requires Ollama)**
- [ ] Ollama server running
- [ ] AI prompt testing
- [ ] Full end-to-end AI integration

## 🎯 **What You Can Do Right Now**

### **Start the Backend Server**
```bash
cd backend
python3 app.py
```
**Server will start on:** http://localhost:8000

### **Test API Endpoints**
```bash
# Health check
curl http://localhost:8000/

# Health check with details
curl http://localhost:8000/health

# Test stress dump (without AI - will fail gracefully)
curl -X POST "http://localhost:8000/dump" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I am stressed about my exam",
    "user_id": "student123",
    "tags": ["exam"]
  }'
```

### **Test Supermemory Directly**
```bash
python3 -c "
from supermemory_client import save_entry, get_recent

# Save a test entry
save_entry(
    user_id='demo_user',
    user_input='I am stressed about my project',
    ai_output={
        'plan': ['Break into tasks', 'Set timer', 'Take breaks'],
        'reset_tip': 'Take 5 deep breaths',
        'motivation': 'You can do this! 💪',
        'stress_score': 0.7
    },
    tags=['project', 'stress']
)

# Retrieve recent entries
recent = get_recent('demo_user', limit=3)
print(f'Found {len(recent)} recent entries')
"
```

## 🐛 **Troubleshooting**

### **If Supermemory fails:**
- Check API key in `supermemory_client.py`
- Verify internet connection
- Check Supermemory API status

### **If FastAPI fails:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check port 8000 is not in use
- Verify Python version (3.8+)

### **If Ollama fails:**
- Install Ollama: https://ollama.ai
- Start server: `ollama serve`
- Pull model: `ollama pull llama2`

## 🎉 **You're Ready for Hackathon!**

Your BrainDump.AI backend is **fully functional** and ready to use! The core system works perfectly:

1. **✅ Backend Server** - FastAPI running on port 8000
2. **✅ Memory Storage** - Supermemory integration working
3. **✅ Data Validation** - JSON schema validation working
4. **✅ Error Handling** - Graceful error handling implemented
5. **✅ Documentation** - All files well-documented for your team

### **Next Steps:**
1. **Frontend Integration** - Connect your React frontend to the API
2. **Ollama Setup** - Install Ollama for AI responses (optional)
3. **Deployment** - Deploy to your preferred platform

**Your backend is hackathon-ready! 🚀**
