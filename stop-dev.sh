#!/bin/bash

# HomeRights AI - Stop Development Servers

echo "🛑 Stopping HomeRights AI Development Environment"
echo "=================================================="

# Kill backend
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo "✓ Backend stopped"
    fi
    rm .backend.pid
fi

# Kill frontend
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✓ Frontend stopped"
    fi
    rm .frontend.pid
fi

# Kill any remaining processes
pkill -f "python wsgi.py" 2>/dev/null || true
pkill -f "ng serve" 2>/dev/null || true

echo ""
echo "✓ All servers stopped"
