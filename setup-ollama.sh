#!/bin/bash

echo "🚀 HomeRights AI - Ollama Integration Setup"
echo "==========================================="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo ""
    echo "Please install Ollama first:"
    echo "  macOS: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  Or visit: https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama is installed"
echo ""

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama service is not running"
    echo "Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ Failed to start Ollama service"
        echo "Please start it manually: ollama serve"
        exit 1
    fi
fi

echo "✅ Ollama service is running"
echo ""

# Check if llama3 model is installed
if ! ollama list | grep -q "llama3"; then
    echo "📥 Downloading llama3 model (this may take a few minutes)..."
    ollama pull llama3
    
    if [ $? -eq 0 ]; then
        echo "✅ llama3 model downloaded successfully"
    else
        echo "❌ Failed to download llama3 model"
        exit 1
    fi
else
    echo "✅ llama3 model is already installed"
fi

echo ""
echo "🔧 Installing Python dependencies..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Make sure Ollama is running: ollama serve"
echo "  2. Start the backend: cd backend && source venv/bin/activate && python wsgi.py"
echo "  3. Start the frontend: cd frontend && npm start"
echo ""
echo "Test Ollama directly:"
echo "  ollama run llama3 'What are tenant rights in the UK?'"
echo ""
