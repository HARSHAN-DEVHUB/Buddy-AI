#!/bin/bash

# Buddy AI - Super Simple Startup Script

echo "🚀 Starting Buddy AI..."
echo ""

# Kill any existing processes
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Start PostgreSQL
echo "1️⃣  Starting PostgreSQL..."
docker-compose up -d postgres
sleep 8

# Run migrations  
echo "2️⃣  Running migrations..."
cd backend
source ../.venv/bin/activate
alembic upgrade head 2>&1 | grep -E "(Running|Upgrade|Current)" || true
cd ..

# Start Backend
echo "3️⃣  Starting Backend (port 8000)..."
cd backend
source ../.venv/bin/activate
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
sleep 3
cd ..

# Start Frontend
echo "4️⃣  Starting Frontend..."
cd frontend  
npm run dev &
sleep 3
cd ..

echo ""
echo "✅ Done! Services starting..."
echo ""
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Run './status.sh' to check status"
echo "Run './stop.sh' to stop everything"
echo ""
