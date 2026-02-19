# HomeRights AI - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher**: [Download Node.js](https://nodejs.org/)
- **MongoDB**: [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git**: [Download Git](https://git-scm.com/downloads)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Home_rights_Ai
```

### 2. Setup MongoDB

Start MongoDB service:

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

**Windows:**
- MongoDB should start automatically after installation
- Or start it from Services

Verify MongoDB is running:
```bash
mongosh
# You should see MongoDB shell
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
python scripts/init_db.py
```

### 4. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python wsgi.py
```

Backend will run on: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Frontend will run on: http://localhost:4200

### 6. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## Using Docker (Alternative)

If you prefer using Docker:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## First Steps

1. **Register an Account**
   - Go to http://localhost:4200/auth/register
   - Create your account

2. **Explore the Chat Interface**
   - Navigate to the chat page
   - Try asking questions about housing rights

3. **Browse Topics**
   - Check out the pre-loaded housing law topics
   - Save topics for later reference

## Troubleshooting

### MongoDB Connection Error

If you see "Connection refused" error:
```bash
# Check if MongoDB is running
mongosh

# If not running, start it:
# macOS:
brew services start mongodb-community
# Linux:
sudo systemctl start mongod
```

### Port Already in Use

If port 5000 or 4200 is already in use:

**Backend (port 5000):**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or change port in wsgi.py
```

**Frontend (port 4200):**
```bash
# Change port in angular.json or use:
ng serve --port 4300
```

### Python Dependencies Error

If you encounter dependency issues:
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies one by one
pip install Flask flask-cors flask-jwt-extended pymongo
```

### Node Modules Error

If npm install fails:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

## Development Tips

### Backend Development

- **Auto-reload**: Flask auto-reloads on code changes in development mode
- **API Testing**: Use Postman or curl to test API endpoints
- **Database GUI**: Use MongoDB Compass to view database

### Frontend Development

- **Hot Reload**: Angular auto-reloads on code changes
- **DevTools**: Use browser DevTools for debugging
- **Angular CLI**: Use `ng generate component <name>` to create components

## Next Steps

1. **Implement ML Features**: Add document classification and OCR
2. **Enhance Chat**: Integrate AI responses
3. **Add More Topics**: Expand the housing law content
4. **Deploy**: Deploy to a cloud platform

## Support

For issues or questions:
- Check the main README.md
- Review the architecture document in docs/req.md
- Create an issue in the repository

## License

This project is for academic purposes.
