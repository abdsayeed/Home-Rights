#!/bin/bash

# HomeRights AI - Simple One-Command Startup
# Just run: ./start.sh

clear
echo "🚀 Starting HomeRights AI..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to check and start MongoDB
start_mongodb() {
    if pgrep -x "mongod" > /dev/null; then
        echo -e "${GREEN}✓${NC} MongoDB already running"
    else
        echo -e "${YELLOW}⚡${NC} Starting MongoDB..."
        
        # Create data directory
        mkdir -p backend/data/db
        
        # Try different MongoDB locations
        if [ -f "/Users/abdullahalsayeed/mongodb-macos-aarch64--8.2.2/bin/mongod" ]; then
            # User's custom MongoDB installation
            nohup /Users/abdullahalsayeed/mongodb-macos-aarch64--8.2.2/bin/mongod --dbpath backend/data/db > logs/mongodb.log 2>&1 &
        elif command -v mongod &> /dev/null; then
            # MongoDB in PATH
            nohup mongod --dbpath backend/data/db > logs/mongodb.log 2>&1 &
        elif command -v brew &> /dev/null; then
            # Try Homebrew
            brew services start mongodb-community > /dev/null 2>&1
        else
            # Try systemd
            sudo systemctl start mongod > /dev/null 2>&1
        fi
        
        sleep 3
        echo -e "${GREEN}✓${NC} MongoDB started"
    fi
}

# Function to check and start Ollama
start_ollama() {
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}⚠${NC}  Ollama not installed (AI chat will use basic responses)"
        echo "   Install: brew install ollama"
        return
    fi
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Ollama already running"
    else
        echo -e "${YELLOW}⚡${NC} Starting Ollama..."
        ollama serve > logs/ollama.log 2>&1 &
        echo $! > .ollama.pid
        sleep 2
        echo -e "${GREEN}✓${NC} Ollama started"
    fi
    
    # Check for llama3 model
    if ! ollama list 2>/dev/null | grep -q "llama3"; then
        echo -e "${YELLOW}⚠${NC}  llama3 model not found"
        echo "   Run: ollama pull llama3"
    fi
}

# Function to start backend
start_backend() {
    echo -e "${YELLOW}⚡${NC} Starting Backend..."
    cd backend
    
    # Create venv with Python 3.12 if needed
    if [ ! -d "venv" ]; then
        if [ -f "/opt/homebrew/bin/python3.12" ]; then
            /opt/homebrew/bin/python3.12 -m venv venv
        else
            python3 -m venv venv
        fi
    fi
    
    # Activate and install dependencies
    source venv/bin/activate
    pip install -q -r requirements.txt 2>/dev/null
    
    mkdir -p uploads logs
    
    # Export environment variables and start
    export FLASK_APP=wsgi.py
    export FLASK_ENV=development
    export MONGODB_URI=mongodb://localhost:27017/homerights
    
    # Start backend with activated venv
    nohup venv/bin/python wsgi.py > ../logs/backend.log 2>&1 &
    echo $! > ../.backend.pid
    cd ..
    echo -e "${GREEN}✓${NC} Backend started"
}

# Function to start frontend
start_frontend() {
    echo -e "${YELLOW}⚡${NC} Starting Frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        npm install > /dev/null 2>&1
    fi
    
    npm start > ../logs/frontend.log 2>&1 &
    echo $! > ../.frontend.pid
    cd ..
    echo -e "${GREEN}✓${NC} Frontend started"
}

# Main execution
mkdir -p logs

echo "Starting services..."
echo ""

start_mongodb
start_ollama
start_backend
start_frontend

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ HomeRights AI is starting!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "🌐 Open in browser: http://localhost:4200"
echo ""
echo "Services:"
echo "  • Frontend: http://localhost:4200"
echo "  • Backend:  http://localhost:5001"
echo "  • Health:   http://localhost:5001/health"
echo ""
echo "To stop: ./stop.sh"
echo ""
echo "Waiting for services to be ready..."

# Wait and check
sleep 8

if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend ready!"
else
    echo -e "${YELLOW}⚡${NC} Backend still starting... (check logs/backend.log)"
fi

if curl -s http://localhost:4200 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend ready!"
else
    echo -e "${YELLOW}⚡${NC} Frontend still starting... (takes ~30 seconds)"
fi

echo ""
echo -e "${GREEN}🎉 Ready! Open http://localhost:4200${NC}"
echo ""
