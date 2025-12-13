#!/bin/bash

# Buddy AI - Status Check Script

echo "📊 Buddy AI Platform Status"
echo "=================================="
echo ""

# Check PostgreSQL
if docker ps | grep -q buddy-ai-postgres; then
    echo "✅ PostgreSQL:  Running"
else
    echo "❌ PostgreSQL:  Stopped"
fi

# Check Backend
if lsof -i:8000 > /dev/null 2>&1; then
    echo "✅ Backend API: Running on http://localhost:8000"
else
    echo "❌ Backend API: Not running"
fi

# Check Frontend
if lsof -i:3001 > /dev/null 2>&1; then
    echo "✅ Frontend:    Running on http://localhost:3001"
elif lsof -i:3000 > /dev/null 2>&1; then
    echo "✅ Frontend:    Running on http://localhost:3000"
else
    echo "❌ Frontend:    Not running"
fi

echo ""
echo "🔗 Quick Links:"
echo "   http://localhost:8000/docs - API Documentation"
echo "   http://localhost:3001      - Frontend Application"
echo ""
