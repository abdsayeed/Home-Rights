# HomeRights AI - Quick Reference Card

## 🚀 Quick Start

```bash
./start-dev.sh          # Start everything
open http://localhost:4200   # Open app
./stop-dev.sh           # Stop everything
```

## 📍 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:4200 |
| Backend | http://localhost:5001 |
| Health Check | http://localhost:5001/health |
| Metrics | http://localhost:5001/metrics |
| API Docs | http://localhost:5001/api |

## 🔑 API Endpoints

### Authentication (No Auth)
```bash
POST /api/auth/register   # Register user
POST /api/auth/login      # Login
```

### Protected (Auth Required)
```bash
GET  /api/auth/me                # Current user
POST /api/documents/upload       # Upload document
POST /api/documents/analyze      # Analyze text
GET  /api/documents              # List documents
POST /api/chat/message           # Send message
GET  /api/chat/sessions          # List sessions
GET  /api/topics                 # List topics
GET  /api/support                # Find support
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:5001/health

# Register user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test1234","firstName":"Test","lastName":"User"}'

# Run all tests
./test-integration.sh
```

## 📂 Project Structure

```
frontend/src/app/
├── core/
│   ├── services/      # API services
│   ├── guards/        # Route guards
│   └── interceptors/  # HTTP interceptors
└── features/          # Feature modules

backend/app/
├── api/               # API endpoints
├── services/          # Business logic
├── ml/                # ML services
└── utils/             # Utilities
```

## 🛠️ Common Commands

### Backend
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python wsgi.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### MongoDB
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

## 🐛 Troubleshooting

### Port in Use
```bash
lsof -ti:5001 | xargs kill -9  # Backend
lsof -ti:4200 | xargs kill -9  # Frontend
```

### MongoDB Not Running
```bash
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

### Dependencies Missing
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

## 📊 Monitoring

### Logs
```bash
tail -f logs/backend.log          # Backend dev log
tail -f logs/frontend.log         # Frontend dev log
tail -f backend/logs/app.log      # Backend app log
tail -f backend/logs/errors.log   # Backend errors
```

### Health & Metrics
```bash
curl http://localhost:5001/health | jq
curl http://localhost:5001/metrics | jq
```

## 🔐 Authentication Flow

1. User registers/logs in
2. Backend returns JWT tokens
3. Frontend stores in localStorage
4. Interceptor adds to all requests
5. Backend validates on protected routes

## 📝 Environment Variables

### Backend (.env)
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGODB_URI=mongodb://localhost:27017/homerights
```

### Frontend (environment.ts)
```typescript
apiUrl: 'http://localhost:5001/api'
```

## 🎯 Features

- ✅ User authentication
- ✅ Document upload & analysis
- ✅ AI chat assistant
- ✅ Housing law topics
- ✅ Support organization finder
- ✅ Health monitoring
- ✅ Performance metrics

## 📚 Documentation

- [README.md](README.md) - Overview
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Integration details
- [INTEGRATION_COMPLETE.md](INTEGRATION_COMPLETE.md) - What was done
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment

## 🆘 Support

1. Check logs
2. Check health endpoint
3. Review documentation
4. Run test script

---

**Quick Start:** `./start-dev.sh` → http://localhost:4200
