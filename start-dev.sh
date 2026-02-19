#!/bin/bash

# HomeRights AI - Development Startup Script
# This script starts both backend and frontend in development mode

set -e

echo "🚀 Starting HomeRights AI Development Environment"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if MongoDB is running
echo -e "\n${BLUE}Checking MongoDB...${NC}"
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${YELLOW}MongoDB is not running. Starting MongoDB...${NC}"
    if command -v brew &> /dev/null; then
        brew services start mongodb-community
    else
        echo -e "${YELLOW}Please start MongoDB manually${NC}"
        echo "Run: sudo systemctl start mongod"
    fi
else
    echo -e "${GREEN}✓ MongoDB is running${NC}"
fi

# Backend setup
echo -e "\n${BLUE}Setting up Backend...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create uploads directory
mkdir -p uploads
mkdir -p logs

# Set environment variables
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export MONGODB_URI=mongodb://localhost:27017/homerights

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Start backend in background
echo -e "\n${BLUE}Starting Backend Server...${NC}"
python wsgi.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo "Backend logs: logs/backend.log"

cd ..

# Frontend setup
echo -e "\n${BLUE}Setting up Frontend...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Start frontend in background
echo -e "\n${BLUE}Starting Frontend Server...${NC}"
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "Frontend logs: logs/frontend.log"

cd ..

# Save PIDs for cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo -e "\n${GREEN}=================================================="
echo "✓ HomeRights AI is starting up!"
echo "==================================================${NC}"
echo ""
echo "📱 Frontend: http://localhost:4200"
echo "🔧 Backend:  http://localhost:5001"
echo "💚 Health:   http://localhost:5001/health"
echo "📊 Metrics:  http://localhost:5001/metrics"
echo ""
echo "Logs:"
echo "  Backend:  logs/backend.log"
echo "  Frontend: logs/frontend.log"
echo ""
echo "To stop the servers, run: ./stop-dev.sh"
echo ""
echo "Waiting for servers to start..."
sleep 5

# Check if servers are running
if curl -s http://localhost:5001/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is ready!${NC}"
else
    echo -e "${YELLOW}⚠ Backend may still be starting...${NC}"
fi

if curl -s http://localhost:4200 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is ready!${NC}"
else
    echo -e "${YELLOW}⚠ Frontend may still be starting (this can take a minute)...${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Development environment is ready!${NC}"
echo "Open http://localhost:4200 in your browser"
