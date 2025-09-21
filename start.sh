#!/bin/bash

# BrainDump.AI - Full Stack Startup Script
# This script starts both the backend and frontend servers

echo "🚀 Starting BrainDump.AI Full Stack Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start Backend Server
echo "🔧 Starting Backend Server..."
cd divyanshu
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Start backend in background
python simple_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start Frontend Server
echo "🎨 Starting Frontend Server..."
cd ..
npm install
npm run dev &
FRONTEND_PID=$!

echo "✅ Both servers are starting up!"
echo "📱 Frontend: http://localhost:8080"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
