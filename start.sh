#!/bin/bash

# Buddy AI - Easy Startup Script
# This script starts the entire platform with one command

set -e

echo "🚀 Starting Buddy AI Platform..."
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Start PostgreSQL
echo -e "${YELLOW}📦 Step 1/5: Starting PostgreSQL Database...${NC}"
docker-compose up -d postgres
echo -e "${GREEN}✓ PostgreSQL started${NC}"
echo ""

# Step 2: Wait for database to be ready
echo -e "${YELLOW}⏳ Step 2/5: Waiting for database to be ready...${NC}"
sleep 5
until docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do
    echo "   Waiting for PostgreSQL..."
    sleep 2
done
echo -e "${GREEN}✓ Database is ready${NC}"
echo ""

# Step 3: Run database migrations
echo -e "${YELLOW}🔄 Step 3/5: Running database migrations...${NC}"
cd backend
source ../.venv/bin/activate 2>/dev/null || python -m venv ../.venv && source ../.venv/bin/activate
pip install -q -r requirements.txt
alembic upgrade head
echo -e "${GREEN}✓ Migrations completed${NC}"
echo ""

# Step 4: Start backend server
echo -e "${YELLOW}⚙️  Step 4/5: Starting backend server...${NC}"
cd /workspaces/Buddy-AI/backend
source /workspaces/Buddy-AI/.venv/bin/activate
nohup python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > /workspaces/Buddy-AI/logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > /workspaces/Buddy-AI/logs/backend.pid
sleep 3
echo -e "${GREEN}✓ Backend server started (PID: $BACKEND_PID)${NC}"
echo ""

# Step 5: Start frontend server
echo -e "${YELLOW}🎨 Step 5/5: Starting frontend server...${NC}"
cd /workspaces/Buddy-AI/frontend
npm install --silent 2>/dev/null || true
nohup npm run dev > /workspaces/Buddy-AI/logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > /workspaces/Buddy-AI/logs/frontend.pid
echo -e "${GREEN}✓ Frontend server started (PID: $FRONTEND_PID)${NC}"
echo ""

# Wait a moment for servers to start
sleep 5

# Display status
echo ""
echo "=================================="
echo -e "${GREEN}✅ Buddy AI Platform is Running!${NC}"
echo "=================================="
echo ""
echo "📊 Services:"
echo "   • PostgreSQL:  Running on port 5432"
echo "   • Backend API: http://localhost:8000"
echo "   • API Docs:    http://localhost:8000/docs"
echo "   • Frontend:    http://localhost:3001"
echo ""
echo "📝 Logs:"
echo "   • Backend:  tail -f logs/backend.log"
echo "   • Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 To stop all services, run: ./stop.sh"
echo ""
