#!/bin/bash

# Buddy AI - Stop Script
# Stops all running services

echo "🛑 Stopping Buddy AI Platform..."
echo "=================================="

# Stop backend
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "✓ Backend server stopped"
    fi
    rm logs/backend.pid
fi

# Stop frontend
if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✓ Frontend server stopped"
    fi
    rm logs/frontend.pid
fi

# Kill any remaining uvicorn/npm processes
pkill -f "uvicorn src.api.main:app" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Stop PostgreSQL
docker-compose down
echo "✓ PostgreSQL stopped"

echo ""
echo "✅ All services stopped"
echo ""
