# HomeRights AI - Project Structure

## 📁 Clean Project Structure

```
homerights-ai/
│
├── 📚 DOCUMENTATION (Essential Only)
│   ├── README.md                    # Quick start & overview
│   ├── COMPLETE_MVP.md              # Complete MVP documentation
│   ├── QUICK_REFERENCE.md           # Quick commands reference
│   └── PROJECT_STRUCTURE.md         # This file
│
├── 🔧 BACKEND (Flask/Python)
│   ├── app/
│   │   ├── __init__.py             # App factory
│   │   ├── config.py               # Configuration
│   │   ├── api/                    # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   ├── topics.py
│   │   │   └── support.py
│   │   ├── services/               # Business logic
│   │   │   ├── chat_service.py
│   │   │   ├── ml_service.py
│   │   │   └── degradation_handler.py
│   │   ├── ml/                     # ML services
│   │   │   ├── document_classifier.py
│   │   │   ├── pattern_detector.py
│   │   │   └── text_extractor.py
│   │   └── utils/                  # Utilities
│   │       ├── validators.py
│   │       ├── retry_strategies.py
│   │       ├── circuit_breaker.py
│   │       ├── logging_config.py
│   │       └── metrics.py
│   ├── scripts/
│   │   └── init_db.py              # Database initialization
│   ├── uploads/                    # Uploaded files (gitignored)
│   │   └── .gitkeep
│   ├── logs/                       # Application logs (gitignored)
│   ├── venv/                       # Virtual environment (gitignored)
│   ├── .env.example                # Environment template
│   ├── Dockerfile                  # Docker configuration
│   ├── requirements.txt            # Python dependencies
│   └── wsgi.py                     # Entry point
│
├── 📱 FRONTEND (Angular 17)
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   │   ├── services/      # API services
│   │   │   │   ├── guards/        # Route guards
│   │   │   │   └── interceptors/  # HTTP interceptors
│   │   │   └── features/          # Feature modules
│   │   │       ├── auth/
│   │   │       ├── chat/
│   │   │       ├── document-upload/
│   │   │       ├── topics/
│   │   │       ├── support/
│   │   │       └── dashboard/
│   │   ├── environments/           # Environment configs
│   │   ├── index.html
│   │   ├── main.ts
│   │   └── styles.scss
│   ├── node_modules/               # Dependencies (gitignored)
│   ├── .angular/                   # Build cache (gitignored)
│   ├── angular.json                # Angular configuration
│   ├── Dockerfile                  # Docker configuration
│   ├── package.json                # Dependencies
│   ├── tsconfig.json               # TypeScript config
│   └── tsconfig.app.json
│
├── 📖 DOCS (Additional Documentation)
│   ├── SETUP.md                    # Detailed setup guide
│   ├── req.md                      # Requirements
│   └── tensorflow.md               # ML documentation
│
├── 🚀 AUTOMATION SCRIPTS
│   ├── start-dev.sh                # Start development servers
│   ├── stop-dev.sh                 # Stop servers
│   └── test-integration.sh         # Run integration tests
│
├── 🐳 DEPLOYMENT
│   └── docker-compose.yml          # Docker Compose config
│
├── 📝 CONFIGURATION
│   ├── .gitignore                  # Git ignore rules
│   └── QUICK_START.md              # Quick start guide
│
└── 📊 RUNTIME (Gitignored)
    └── logs/                       # Runtime logs
        └── .gitkeep
```

## 🧹 Cleaned Up Items

### Removed Files
- ❌ Duplicate documentation (15 files)
- ❌ Python cache files (__pycache__)
- ❌ Test upload files
- ❌ Build caches
- ❌ System files (.DS_Store)
- ❌ Runtime logs
- ❌ Duplicate venv (backend/backend/)

### Kept Essential Files
- ✅ README.md - Main documentation
- ✅ COMPLETE_MVP.md - Complete MVP guide
- ✅ QUICK_REFERENCE.md - Quick commands
- ✅ All source code files
- ✅ Configuration files
- ✅ Automation scripts

## 📊 Project Size

### Before Cleanup
- Documentation: 15+ files
- Total size: ~500MB+ (with node_modules, venv)
- Tracked files: Many duplicates

### After Cleanup
- Documentation: 4 essential files
- Source code: Clean and organized
- Gitignored: All build artifacts, caches, logs
- Result: Lighter, cleaner, better organized

## 🎯 Benefits

1. **Cleaner Repository**
   - No duplicate documentation
   - No build artifacts
   - No cache files

2. **Faster Git Operations**
   - Smaller repository size
   - Faster clones
   - Faster commits

3. **Better Organization**
   - Clear structure
   - Essential docs only
   - Easy to navigate

4. **Easier Maintenance**
   - Less confusion
   - Clear purpose for each file
   - Better for collaboration

## 📚 Documentation Guide

### For Quick Start
→ Read **README.md**

### For Complete Reference
→ Read **COMPLETE_MVP.md**

### For Quick Commands
→ Read **QUICK_REFERENCE.md**

### For Project Structure
→ Read **PROJECT_STRUCTURE.md** (this file)

## 🔧 Development Workflow

```bash
# 1. Clone repository
git clone <repo-url>
cd homerights-ai

# 2. Start development
./start-dev.sh

# 3. Open application
open http://localhost:4200

# 4. Stop when done
./stop-dev.sh
```

## 📝 Notes

- All build artifacts are gitignored
- Logs are gitignored but directories are tracked
- Virtual environments are gitignored
- Node modules are gitignored
- Upload files are gitignored (except .gitkeep)

## 🎉 Result

A clean, well-organized, production-ready MVP with:
- ✅ Essential documentation only
- ✅ Clean git history
- ✅ Proper gitignore
- ✅ Organized structure
- ✅ Easy to maintain
- ✅ Ready for collaboration

---

**Version:** 2.0.0  
**Status:** ✅ Clean & Optimized  
**Last Updated:** February 17, 2026
