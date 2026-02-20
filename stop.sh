#!/bin/bash

# HomeRights AI - Simple Stop Script
# Just run: ./stop.sh

clear
echo "🛑 Stopping HomeRights AI..."
echo ""

GREEN='\033[0;32m'
NC='\033[0m'

# Stop backend
if [ -f .backend.pid ]; then
    kill $(cat .backend.pid) 2>/dev/null
    rm .backend.pid
    echo -e "${GREEN}✓${NC} Backend stopped"
fi

# Stop frontend
if [ -f .frontend.pid ]; then
    kill $(cat .frontend.pid) 2>/dev/null
    rm .frontend.pid
    echo -e "${GREEN}✓${NC} Frontend stopped"
fi

# Stop Ollama if we started it
if [ -f .ollama.pid ]; then
    kill $(cat .ollama.pid) 2>/dev/null
    rm .ollama.pid
    echo -e "${GREEN}✓${NC} Ollama stopped"
fi

# Stop MongoDB
if pgrep -x "mongod" > /dev/null; then
    pkill -x mongod 2>/dev/null
    echo -e "${GREEN}✓${NC} MongoDB stopped"
fi

# Kill any remaining processes
pkill -f "python wsgi.py" 2>/dev/null
pkill -f "ng serve" 2>/dev/null

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
