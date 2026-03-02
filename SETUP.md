# 🚀 HomeRights AI - Complete Setup Guide

This guide will walk you through setting up and running the HomeRights AI project from scratch.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Accessing the Application](#accessing-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Development Workflow](#development-workflow)
7. [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Python 3.8 or higher**
   - Check version: `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 18 or higher**
   - Check version: `node --version`
   - Download: https://nodejs.org/

3. **MongoDB 6.0 or higher**
   - Check if installed: `mongod --version`
   - Download: https://www.mongodb.com/try/download/community

4. **Git**
   - Check version: `git --version`
   - Download: https://git-scm.com/downloads

### Optional (for AI Chat Feature)

5. **Ollama** (for AI-powered chat)
   - Check if installed: `ollama --version`
   - Download: https://ollama.ai/download
   - After installation, pull the model: `ollama pull llama3.2`

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/abdsayeed/Home-Rights.git
cd Home-Rights
```

### Step 2: Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create Python virtual environment:**
```bash
python3 -m venv venv
```

3. **Activate virtual environment:**

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create environment file (optional):**
```bash
cp .env.example .env
```

Edit `.env` if you need custom configuration:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
MONGODB_URI=mongodb://localhost:27017/homerights
OLLAMA_API_URL=http://localhost:11434
```

6. **Return to project root:**
```bash
cd ..
```

### Step 3: Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install Node.js dependencies:**
```bash
npm install
```

3. **Return to project root:**
```bash
cd ..
```

### Step 4: Database Setup

1. **Ensure MongoDB is running:**

**On macOS (if installed via Homebrew):**
```bash
brew services start mongodb-community
```

**On Linux:**
```bash
sudo systemctl start mongod
```

**On Windows:**
- MongoDB should start automatically as a service
- Or run: `net start MongoDB`

2. **Verify MongoDB is running:**
```bash
mongosh
```
If it connects successfully, type `exit` to quit.

3. **Create admin user and seed data:**
```bash
python3 backend/scripts/create_admin.py
```

This will:
- Create an admin user (admin@homerights.ai / Admin123!)
- Add 15 housing law topics
- Add 15 UK support organizations

4. **Setup database indexes (optional but recommended):**
```bash
python3 backend/scripts/setup_indexes.py
```

---

## Running the Application

### Option 1: Quick Start (Recommended)

Use the provided start script that launches all services:

```bash
./start.sh
```

This will:
- Start MongoDB (if not running)
- Start the Flask backend on port 5001
- Start the Angular frontend on port 4200
- Check Ollama status (if installed)

**To stop all services:**
```bash
./stop.sh
```

### Option 2: Manual Start (For Development)

If you prefer to run services separately:

#### Terminal 1 - MongoDB
```bash
# Usually runs automatically, but you can start manually:
mongod --dbpath backend/data/db
```

#### Terminal 2 - Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python wsgi.py
```

Backend will run on: http://localhost:5001

#### Terminal 3 - Frontend
```bash
cd frontend
npm start
```

Frontend will run on: http://localhost:4200

#### Terminal 4 - Ollama (Optional)
```bash
ollama serve
```

Ollama will run on: http://localhost:11434

---

## Accessing the Application

Once all services are running:

### Frontend Application
Open your browser and go to: **http://localhost:4200**

### Admin Dashboard

1. **Login with admin credentials:**
   - Go to: http://localhost:4200/auth/login
   - Email: `admin@homerights.ai`
   - Password: `Admin123!`

2. **Access admin panel:**
   - After login, click the **"⚙️ Admin"** button in the navigation bar
   - Or go directly to: http://localhost:4200/admin

### Backend API
- API Base URL: http://localhost:5001
- Health Check: http://localhost:5001/health
- API Documentation: See README.md for endpoint details

### Regular User Access

1. **Register a new account:**
   - Go to: http://localhost:4200/auth/register
   - Fill in your details
   - Login with your credentials

2. **Explore features:**
   - Browse housing law topics
   - Upload and analyze documents
   - Chat with AI assistant
   - Find support organizations

---

## Troubleshooting

### MongoDB Issues

**Problem: MongoDB won't start**
```bash
# Check if MongoDB is already running
ps aux | grep mongod

# Check MongoDB logs
tail -f /usr/local/var/log/mongodb/mongo.log  # macOS
tail -f /var/log/mongodb/mongod.log           # Linux

# Try starting with specific data directory
mongod --dbpath backend/data/db
```

**Problem: Connection refused**
- Ensure MongoDB is running: `mongosh`
- Check if port 27017 is in use: `lsof -i :27017`

### Backend Issues

**Problem: Backend won't start**
```bash
# Check if virtual environment is activated
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install --upgrade -r backend/requirements.txt

# Check if port 5001 is available
lsof -i :5001
```

**Problem: Import errors**
```bash
# Ensure you're in the backend directory with venv activated
cd backend
source venv/bin/activate
python -c "import flask; print(flask.__version__)"
```

### Frontend Issues

**Problem: Frontend won't start**
```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Check Node version (must be 18+)
node --version
```

**Problem: Port 4200 already in use**
```bash
# Kill process on port 4200
lsof -ti:4200 | xargs kill -9

# Or use a different port
ng serve --port 4300
```

### Ollama Issues

**Problem: AI chat not working**
```bash
# Check if Ollama is installed
ollama --version

# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull the model
ollama pull llama3.2
```

**Problem: Model not found**
```bash
# List installed models
ollama list

# Pull the required model
ollama pull llama3.2
```

### Admin Login Issues

**Problem: Can't login as admin**
```bash
# Recreate admin user
python3 backend/scripts/create_admin.py

# Verify admin exists in database
mongosh homerights --eval "db.users.findOne({email: 'admin@homerights.ai'})"
```

**Problem: Admin dashboard shows no data**
- Ensure backend is running on port 5001
- Check browser console for errors (F12)
- Verify you're logged in with admin role
- Run seed script again: `python3 backend/scripts/create_admin.py`

### Permission Issues

**Problem: Permission denied errors**
```bash
# On macOS/Linux, ensure scripts are executable
chmod +x start.sh stop.sh

# Ensure MongoDB data directory is writable
chmod -R 755 backend/data/db
```

---

## Development Workflow

### Making Changes to Backend

1. **Activate virtual environment:**
```bash
cd backend
source venv/bin/activate
```

2. **Make your changes to Python files**

3. **Restart backend:**
```bash
# Stop current backend (Ctrl+C)
python wsgi.py
```

### Making Changes to Frontend

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Make your changes to TypeScript/HTML/SCSS files**

3. **Changes auto-reload** (if using `npm start`)

### Adding New Dependencies

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install <package-name>
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install <package-name>
```

### Database Management

**View data in MongoDB:**
```bash
mongosh homerights
db.users.find().pretty()
db.topics.find().pretty()
db.support_orgs.find().pretty()
```

**Clear all data:**
```bash
mongosh homerights --eval "db.dropDatabase()"
python3 backend/scripts/create_admin.py
```

**Backup database:**
```bash
mongodump --db homerights --out backup/
```

**Restore database:**
```bash
mongorestore --db homerights backup/homerights/
```

---

## Project Structure

```
Home-Rights/
├── backend/                    # Flask backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   ├── admin.py       # Admin routes
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── chat.py        # AI chat
│   │   │   ├── documents.py   # Document upload
│   │   │   ├── support.py     # Support orgs
│   │   │   └── topics.py      # Topics
│   │   ├── ml/                # ML models
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utilities
│   ├── data/db/               # MongoDB data
│   ├── scripts/               # Setup scripts
│   ├── uploads/               # Uploaded files
│   ├── venv/                  # Python virtual env
│   ├── requirements.txt       # Python dependencies
│   └── wsgi.py               # Entry point
│
├── frontend/                   # Angular frontend
│   ├── src/app/
│   │   ├── core/              # Services & guards
│   │   │   ├── services/      # API services
│   │   │   └── guards/        # Route guards
│   │   └── features/          # Feature modules
│   │       ├── admin/         # Admin dashboard
│   │       ├── auth/          # Login/Register
│   │       ├── chat/          # AI chat
│   │       ├── documents/     # Document upload
│   │       ├── support/       # Support finder
│   │       └── topics/        # Topics browser
│   ├── package.json           # NPM dependencies
│   └── angular.json           # Angular config
│
├── start.sh                    # Start all services
├── stop.sh                     # Stop all services
├── README.md                   # Project documentation
├── SETUP.md                    # This file
└── MVP_COMPLETE.md            # Complete MVP docs
```

---

## Environment Variables

### Backend (.env)

Create `backend/.env` file:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-change-in-production
FLASK_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/homerights

# Ollama (AI Chat)
OLLAMA_API_URL=http://localhost:11434

# File Upload
MAX_CONTENT_LENGTH=10485760  # 10MB in bytes
UPLOAD_FOLDER=uploads

# Security
JWT_ACCESS_TOKEN_EXPIRES=7200  # 2 hours in seconds
```

### Frontend (environment.ts)

Located at `frontend/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5001'
};
```

---

## Testing the Setup

### 1. Test Backend API

```bash
# Health check
curl http://localhost:5001/health

# Get topics
curl http://localhost:5001/api/topics

# Get support organizations
curl http://localhost:5001/api/support
```

### 2. Test Frontend

1. Open http://localhost:4200
2. You should see the homepage
3. Try navigating to different pages

### 3. Test Admin Dashboard

1. Login at http://localhost:4200/auth/login
2. Use credentials: admin@homerights.ai / Admin123!
3. Click "⚙️ Admin" button
4. Verify you can see:
   - Dashboard with metrics
   - Users list
   - Topics list (15 topics)
   - Organizations list (15 organizations)

### 4. Test AI Chat (if Ollama installed)

1. Go to http://localhost:4200/chat
2. Type a question about tenant rights
3. You should get an AI response

---

## Production Deployment

For production deployment, see the deployment section in README.md or MVP_COMPLETE.md.

Key considerations:
- Use environment variables for secrets
- Enable HTTPS
- Use production database
- Configure CORS properly
- Set up monitoring and logging
- Use process managers (PM2, systemd)
- Set up reverse proxy (Nginx)

---

## Getting Help

If you encounter issues:

1. **Check the logs:**
   - Backend: Terminal output where backend is running
   - Frontend: Browser console (F12)
   - MongoDB: `/var/log/mongodb/mongod.log`

2. **Common commands:**
   ```bash
   # Check running processes
   ps aux | grep -E "(mongod|python|node)"
   
   # Check ports in use
   lsof -i :4200 -i :5001 -i :27017
   
   # View MongoDB data
   mongosh homerights
   ```

3. **Reset everything:**
   ```bash
   ./stop.sh
   mongosh homerights --eval "db.dropDatabase()"
   python3 backend/scripts/create_admin.py
   ./start.sh
   ```

4. **Contact:**
   - GitHub Issues: https://github.com/abdsayeed/Home-Rights/issues
   - Email: support@homerights.ai

---

## Quick Reference

### Start Application
```bash
./start.sh
```

### Stop Application
```bash
./stop.sh
```

### Reset Database
```bash
python3 backend/scripts/create_admin.py
```

### Admin Credentials
- Email: `admin@homerights.ai`
- Password: `Admin123!`

### URLs
- Frontend: http://localhost:4200
- Backend: http://localhost:5001
- Admin: http://localhost:4200/admin

---

## Next Steps

After successful setup:

1. ✅ Explore the admin dashboard
2. ✅ Create new topics and organizations
3. ✅ Test document upload and analysis
4. ✅ Try the AI chat feature
5. ✅ Register as a regular user and test features
6. ✅ Review the codebase and make customizations

---

**Happy Coding! 🎉**

For more detailed information, see:
- README.md - Project overview and features
- MVP_COMPLETE.md - Complete MVP documentation
- docs/SETUP.md - Additional setup guides
