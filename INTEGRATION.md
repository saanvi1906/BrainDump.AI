# BrainDump.AI - Full Stack Integration

A complete full-stack application that transforms stress into actionable plans using AI.

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **State Management**: React Query (TanStack Query)
- **API Communication**: Custom API client with error handling

## 🚀 Quick Start

### Option 1: Use the Startup Script (Recommended)
```bash
./start.sh
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd divyanshu
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
npm install
npm run dev
```

## 📡 API Integration

### Endpoints
- `GET /health` - Health check
- `POST /dumps` - Create new brain dump
- `GET /dumps` - List all dumps

### Frontend Integration
- **API Client**: `src/lib/api.ts` - Handles all HTTP requests
- **React Query Hooks**: `src/hooks/use-api.ts` - Manages API state
- **Error Handling**: Automatic error handling with toast notifications
- **Loading States**: Integrated loading states for better UX

### Data Flow
1. User inputs stress text in `BrainDumpInput`
2. Frontend calls `useCreateDump` hook
3. API client sends POST request to `/dumps`
4. Backend processes text with AI service
5. Response is transformed and displayed in `ResultCards`
6. Mood entries are updated based on stress score

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file in the root directory:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend Configuration
The backend uses environment variables from `.env` file:
- `DATABASE_URL`: SQLite database path
- `APP_CORS_ORIGINS`: Allowed CORS origins

## 📁 Project Structure

```
BrainDump.AI/
├── src/                    # Frontend React app
│   ├── components/         # UI components
│   ├── hooks/             # Custom hooks (including API hooks)
│   ├── lib/               # Utilities (including API client)
│   └── pages/             # Page components
├── divyanshu/             # Backend FastAPI app
│   ├── app/
│   │   ├── routers/       # API routes
│   │   ├── services/      # Business logic
│   │   ├── models.py      # Database models
│   │   └── main.py        # FastAPI app
│   └── requirements.txt   # Python dependencies
└── start.sh              # Startup script
```

## 🎯 Key Features

### Frontend Features
- **Real-time API Integration**: Live data from backend
- **Error Handling**: User-friendly error messages
- **Loading States**: Smooth loading indicators
- **Responsive Design**: Mobile-first approach
- **Voice Input**: Speech-to-text functionality

### Backend Features
- **AI Processing**: Intelligent stress analysis
- **Database Storage**: Persistent dump storage
- **CORS Support**: Cross-origin requests
- **Health Monitoring**: API health checks
- **Crisis Detection**: Safety features for mental health

## 🔍 Testing the Integration

1. Start both servers using `./start.sh`
2. Open http://localhost:5173 in your browser
3. Enter some stress text in the input field
4. Click "Transform My Chaos"
5. Verify the results are displayed correctly
6. Check the backend logs for API calls

## 🛠️ Development

### Adding New API Endpoints
1. Add route in `divyanshu/app/routers/`
2. Create corresponding hook in `src/hooks/use-api.ts`
3. Update API client in `src/lib/api.ts` if needed

### Modifying Components
- All components are in `src/components/`
- Use the API hooks for data fetching
- Follow the existing error handling patterns

## 📊 Data Models

### Frontend Types
```typescript
interface DumpResult {
  actionPlan: string[];
  wellnessReset: string;
  motivationBoost: string;
}
```

### Backend Models
```python
class Dump(Base):
    id: int
    text: str
    action_plan: str
    wellness_tip: str
    motivation: str
    stress_score: float
    created_at: datetime
```

## 🚨 Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure backend CORS settings allow frontend origin
2. **API Connection Failed**: Check if backend is running on port 8000
3. **Database Errors**: Verify SQLite database permissions
4. **Build Errors**: Run `npm install` to update dependencies

### Debug Mode
- Frontend: Check browser console for errors
- Backend: Check terminal output for API logs
- API Docs: Visit http://localhost:8000/docs for interactive API testing

## 🎉 Success!

Your BrainDump.AI application is now fully integrated! The frontend communicates seamlessly with the backend, providing a complete stress-to-success transformation experience.
