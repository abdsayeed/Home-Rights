# HomeRights AI - Intelligent Housing Rights Assistant

An AI-powered platform that helps UK tenants understand their housing rights, analyze legal documents, and find support services.

> **Status:** ✅ Complete MVP with Ollama LLM | **Version:** 2.1.0 | **Clean & Optimized**

## 🚀 Quick Start

> **New to the project?** Check `QUICK_START.txt` for a visual guide!

### One-Time Setup

```bash
# 1. Install Ollama (for AI features)
brew install ollama

# 2. Download AI model
ollama pull llama3

# 3. Run setup
./setup-ollama.sh

# 4. (Optional) Setup easy commands
./setup-alias.sh
```

### Start the App

**Option 1: Simple command**
```bash
./start.sh
```

**Option 2: Double-click (macOS)**
- Double-click `launch-app.command` in Finder

**Option 3: From anywhere (after running setup-alias.sh)**
```bash
homerights
```

**Access the app:** http://localhost:4200

### Stop the App

```bash
./stop.sh
# or: homerights-stop
```

That's it! 🎉

## � Documentation

- **README.md** (this file) - Complete guide
- **COMPLETE_MVP.md** - Detailed MVP documentation
- **QUICK_REFERENCE.md** - Quick commands reference
- **PROJECT_STRUCTURE.md** - Project structure guide

## 🎯 Quick Commands

```bash
# Start everything
./start.sh

# Stop everything
./stop.sh

# Clear documents (if you want to re-upload/re-analyze)
./clear-documents.sh

# Setup easy commands (run once)
./setup-alias.sh

# Then use from anywhere:
homerights        # Start
homerights-stop   # Stop

# Test AI integration
cd backend && source venv/bin/activate && python test_ollama.py

# View logs
tail -f logs/backend.log
tail -f logs/frontend.log
```

## 📋 Features

### 🤖 AI Chat Assistant (Enhanced with Ollama!)
- **Local LLM powered by Llama 3** - Natural, context-aware conversations
- Intelligent conversational AI for housing law questions
- Context-aware responses with conversation history
- Intent detection and smart routing
- Session management
- Fallback to rule-based responses if LLM unavailable
- **Privacy-first**: All processing happens locally, no data sent to external servers

### 📄 Document Analysis (ML + LLM Enhanced)
- Upload PDF, JPG, PNG documents
- OCR text extraction
- ML-powered classification
- Pattern detection for legal issues
- **LLM-enhanced explanations** - Natural language analysis of detected issues
- Risk assessment (Critical/High/Medium/Low)
- Actionable recommendations
- 3-tier graceful degradation

### 📚 Housing Law Topics
- Comprehensive UK housing law database
- Categorized topics
- Search functionality
- Related topics linking

### 🆘 Support Finder
- Find local housing support organizations
- Filter by location and issue type
- Contact information
- Service descriptions

### 🔐 Authentication
- Secure JWT-based authentication
- User registration and login
- Protected routes
- Token refresh

## 🏗️ Architecture

```
Frontend (Angular 17)  →  Backend (Flask)  →  MongoDB
    ↓                         ↓                  ↓
Components              API Endpoints        Collections
Services                ML Services          - users
Guards                  Ollama LLM (NEW!)    - documents
Interceptors            Circuit Breakers     - chat_sessions
                        Retry Logic          - topics
                        Logging              - support_orgs
                        Metrics
```

### AI Architecture (NEW!)

```
User Question
     ↓
Chat Service (Intent Detection)
     ↓
     ├─→ Document Text? → ML Analysis + Ollama Enhancement
     ├─→ Conversational? → Ollama LLM (with context)
     └─→ Ollama Fails? → Rule-based Fallback
```

## 📁 Project Structure

```
.
├── frontend/                 # Angular 17 application
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/        # Services, guards, interceptors
│   │   │   └── features/    # Feature modules
│   │   └── environments/    # Environment configs
│   └── package.json
│
├── backend/                  # Flask application
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   ├── ml/              # ML services
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   ├── requirements.txt
│   └── wsgi.py
│
├── docs/                     # Documentation
├── logs/                     # Application logs
├── start-dev.sh             # Development startup script
├── stop-dev.sh              # Stop development servers
└── INTEGRATION_GUIDE.md     # Detailed integration docs
```

## 🔧 Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p uploads logs

# Set environment variables
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export MONGODB_URI=mongodb://localhost:27017/homerights

# Start server
python wsgi.py
```

Backend runs on: http://localhost:5001

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: http://localhost:4200

### MongoDB Setup

```bash
# macOS (with Homebrew)
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Linux (Ubuntu/Debian)
sudo apt-get install mongodb
sudo systemctl start mongod

# Verify
mongo --eval "db.version()"
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Documents
- `POST /api/documents/upload` - Upload & analyze document
- `POST /api/documents/analyze` - Analyze text
- `GET /api/documents` - List documents
- `GET /api/documents/:id` - Get document

### Chat
- `POST /api/chat/message` - Quick message
- `GET /api/chat/sessions` - List sessions
- `POST /api/chat/sessions` - Create session
- `POST /api/chat/sessions/:id/messages` - Send message

### Topics
- `GET /api/topics` - List topics
- `GET /api/topics/:id` - Get topic
- `GET /api/topics/categories` - List categories

### Support
- `GET /api/support` - Find organizations
- `GET /api/support/:id` - Get organization

### Monitoring
- `GET /health` - Health check
- `GET /metrics` - Performance metrics

## 🛡️ Production Features

### Backend
- ✅ Structured JSON logging
- ✅ Request tracing
- ✅ Circuit breaker pattern
- ✅ Retry strategies with exponential backoff
- ✅ Graceful degradation (3-tier fallback)
- ✅ File validation & security
- ✅ Duplicate detection
- ✅ Metrics collection
- ✅ Health monitoring

### Frontend
- ✅ JWT authentication
- ✅ HTTP interceptors
- ✅ Route guards
- ✅ Reactive state management
- ✅ Error handling
- ✅ Loading states
- ✅ Responsive design

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:5001/health | jq
```

Response includes:
- Database status
- ML service status
- Circuit breaker states
- Version info

### Metrics
```bash
curl http://localhost:5001/metrics | jq
```

Includes:
- Document upload counts
- Processing times
- Error rates
- Active tasks

### Logs
```bash
# Backend application logs
tail -f backend/logs/app.log

# Backend errors only
tail -f backend/logs/errors.log

# Development server logs
tail -f logs/backend.log
tail -f logs/frontend.log
```

## 🧪 Testing

### Test Ollama Integration
```bash
cd backend
source venv/bin/activate
python test_ollama.py  # Tests AI chat integration
```

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security

- JWT-based authentication
- Password hashing (Werkzeug)
- File validation (MIME type, size, structure)
- CORS protection
- Input validation
- SQL injection prevention (MongoDB)
- XSS protection

## 🚀 Deployment

### Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Stop services
docker-compose down
```

### Manual Deployment

See `docs/SETUP.md` for detailed deployment instructions.

## 📖 Documentation

- [Integration Guide](INTEGRATION_GUIDE.md) - Frontend-Backend integration
- [Implementation Progress](IMPLEMENTATION_PROGRESS.md) - Feature status
- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Architecture](arch.md) - System architecture

## 🐛 Troubleshooting

### Document Analysis Not Working

**Issue:** Documents not being analyzed after upload

**Solution:**
1. Check if you're uploading the same file multiple times:
   ```bash
   # The system detects duplicates by file hash
   # Clear previous uploads to re-analyze:
   ./clear-documents.sh
   ```

2. Verify ML service is running:
   ```bash
   curl http://localhost:5001/health | jq '.ml_service'
   # Should show: "operational"
   ```

3. Test with text analysis first:
   ```bash
   python3 test-document-upload.py
   # This will test the entire pipeline
   ```

4. Check backend logs:
   ```bash
   tail -f logs/backend.log
   # Look for "Document upload request received" and "Document processed successfully"
   ```

5. Verify Python 3.12 is being used:
   ```bash
   cd backend && source venv/bin/activate && python --version
   # Should show: Python 3.12.x
   ```

**Common Issues:**
- **Duplicate Detection**: If you upload the same file twice, it returns the previous analysis. This is expected behavior.
- **TensorFlow Not Working**: Make sure you're using Python 3.12 in the virtual environment (not system Python 3.14)
- **OCR Failing**: For scanned PDFs/images, ensure Tesseract is installed: `brew install tesseract`

### Ollama Issues
```bash
# Ollama not found
brew install ollama  # Install Ollama

# Model not found
ollama pull llama3  # Download model

# Service not running
ollama serve  # Start Ollama service

# Test connection
curl http://localhost:11434/api/tags
```

### CORS Errors
Backend CORS is configured for `http://localhost:4200`. Update in `backend/app/__init__.py` if needed.

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
pgrep mongod

# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

### Port Already in Use
```bash
# Kill process on port 5001 (backend)
lsof -ti:5001 | xargs kill -9

# Kill process on port 4200 (frontend)
lsof -ti:4200 | xargs kill -9
```

### Module Not Found
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👥 Team

Developed as part of a housing rights initiative to help UK tenants understand and exercise their legal rights.

## 🔗 Links

- [Frontend Documentation](frontend/README.md)
- [Backend API Documentation](backend/README.md)
- [Integration Guide](INTEGRATION_GUIDE.md)

## 📞 Support

For issues or questions:
1. Check the [COMPLETE_MVP.md](COMPLETE_MVP.md) documentation
2. Review logs in `backend/logs/` and `logs/`
3. Check the health endpoint: http://localhost:5001/health
4. Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands

## 🧹 Project Cleanup

This project has been optimized and cleaned:
- ✅ Removed 15+ duplicate documentation files
- ✅ Cleaned Python cache files (__pycache__)
- ✅ Removed test upload files
- ✅ Cleaned build caches
- ✅ Updated .gitignore for better tracking
- ✅ Kept only essential documentation (4 files)
- ✅ Result: Lighter, cleaner, better organized

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for details.

---

**Built with ❤️ for UK tenants**
