# 🏠 HomeRights AI

**AI-Powered UK Tenant Rights Platform**

A comprehensive web application that helps UK tenants understand their rights, analyze rental documents, and find support organizations using AI technology.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Admin Dashboard](#-admin-dashboard)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

### For Tenants
- **🤖 AI Chat Assistant** - Get instant answers about tenant rights using Ollama LLM
- **📄 Document Analysis** - Upload and analyze rental contracts with ML-powered risk detection
- **📚 Knowledge Base** - Browse comprehensive housing law topics and guides
- **🏢 Support Finder** - Find local housing support organizations with geo-spatial search
- **👤 User Dashboard** - Track your documents, saved topics, and chat history

### For Administrators
- **📊 Admin Dashboard** - View system metrics and KPIs
- **👥 User Management** - Manage users and roles
- **📝 Content Management** - Create, edit, and publish housing law topics
- **🏢 Organization Management** - Manage support organizations and verification
- **📋 Audit Logs** - Track all admin actions for compliance

---

## 🛠 Tech Stack

### Frontend
- **Angular 17** - Modern web framework
- **TypeScript** - Type-safe JavaScript
- **RxJS** - Reactive programming
- **SCSS** - Styling

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database
- **Ollama** - Local LLM for AI chat
- **PyMongo** - MongoDB driver
- **JWT** - Authentication

### ML/AI
- **Ollama (Llama 3.2)** - Language model for chat
- **scikit-learn** - Document classification
- **PyPDF2** - PDF text extraction

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB 6.0+
- Ollama (optional, for AI chat features)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/abdsayeed/Home-Rights.git
cd Home-Rights
```

2. **Setup backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

3. **Setup frontend:**
```bash
cd frontend
npm install
cd ..
```

4. **Create admin user and seed data:**
```bash
python3 backend/scripts/create_admin.py
```

5. **Start all services:**
```bash
./start.sh
```

### Access the Application

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:5001
- **Admin Dashboard**: http://localhost:4200/admin

### Login Credentials

**Admin User:**
- Email: `admin@homerights.ai`
- Password: `Admin123!`

**Regular User:**
- Register at http://localhost:4200/auth/register

### Stop Services
```bash
./stop.sh
```

---

**📖 For detailed setup instructions, troubleshooting, and development guide, see [SETUP.md](SETUP.md)**

---

---

## 🔐 Admin Dashboard

### Access
1. Login with admin credentials
2. Click the **"⚙️ Admin"** button in the navigation bar
3. You'll see the admin dashboard with metrics and management options

### Features

#### Dashboard Overview
- View system-wide metrics (users, documents, topics, organizations, chat messages)
- Filter by time period (7 days, 30 days, 90 days)
- Quick action links to management pages

#### User Management (`/admin/users`)
- View all users with pagination
- Search by name or email
- Filter by role
- Change user roles (super_admin only)
- Roles: `user`, `super_admin`, `content_admin`, `support_admin`, `read_only`

#### Topics Management (`/admin/topics`)
- Create, edit, and delete housing law topics
- Filter by category and publication status
- Publish/unpublish topics
- Add tags and categorize content
- Categories: eviction, deposits, repairs, rent, rights

#### Organizations Management (`/admin/support`)
- Create, edit, and delete support organizations
- Verify organizations
- Filter by type and verification status
- Toggle accepting referrals status
- Types: charity, advice_center, legal_aid, council

### Admin Roles

| Role | Permissions |
|------|-------------|
| `super_admin` | Full access to all features |
| `content_admin` | Manage topics only |
| `support_admin` | Manage organizations only |
| `read_only` | View-only access |
| `user` | Regular user (no admin access) |

---

## 📁 Project Structure

```
Home-Rights/
├── backend/                    # Python Flask backend
│   ├── app/
│   │   ├── api/               # API endpoints (auth, chat, documents, topics, support, admin)
│   │   ├── ml/                # ML models (document classifier, pattern detector)
│   │   ├── services/          # Business logic (chat, ollama, ML services)
│   │   └── utils/             # Utilities (admin decorators, circuit breaker, validators)
│   ├── data/db/               # MongoDB data directory
│   ├── scripts/               # Setup scripts (create_admin.py, setup_indexes.py)
│   ├── uploads/               # Uploaded document files
│   ├── venv/                  # Python virtual environment
│   ├── requirements.txt       # Python dependencies
│   └── wsgi.py               # WSGI entry point
│
├── frontend/                   # Angular 17 frontend
│   ├── src/app/
│   │   ├── core/              # Core services and guards
│   │   │   ├── services/      # API services (auth, admin, chat, document, topic, support)
│   │   │   └── guards/        # Route guards (auth.guard, admin.guard)
│   │   └── features/          # Feature modules
│   │       ├── admin/         # Admin dashboard (users, topics, organizations)
│   │       ├── auth/          # Authentication (login, register)
│   │       ├── chat/          # AI chat interface
│   │       ├── documents/     # Document upload and analysis
│   │       ├── support/       # Support organization finder
│   │       └── topics/        # Housing law topics browser
│   ├── package.json           # NPM dependencies
│   └── angular.json           # Angular configuration
│
├── docs/                       # Documentation
├── start.sh                    # Start all services script
├── stop.sh                     # Stop all services script
├── README.md                   # This file
├── SETUP.md                    # Detailed setup guide
└── MVP_COMPLETE.md            # Complete MVP documentation
```

---

## 🔌 API Documentation

### Authentication
```
POST /api/auth/register        # Register new user
POST /api/auth/login           # Login user
GET  /api/auth/me              # Get current user
```

### Topics
```
GET  /api/topics               # List all topics
GET  /api/topics/:slug         # Get topic by slug
POST /api/topics/:id/view      # Track topic view
```

### Documents
```
POST /api/documents/upload     # Upload document
GET  /api/documents            # List user documents
GET  /api/documents/:id        # Get document details
```

### Support Organizations
```
GET  /api/support              # List organizations
GET  /api/support/search       # Search by location
```

### Chat
```
POST /api/chat/message         # Send chat message
GET  /api/chat/history         # Get chat history
```

### Admin (Protected)
```
GET  /api/admin/dashboard/overview    # Dashboard metrics
GET  /api/admin/users                 # List users
PATCH /api/admin/users/:id/role       # Update user role
GET  /api/admin/topics                # List all topics
POST /api/admin/topics                # Create topic
PUT  /api/admin/topics/:id            # Update topic
DELETE /api/admin/topics/:id          # Delete topic
GET  /api/admin/support               # List organizations
POST /api/admin/support               # Create organization
PUT  /api/admin/support/:id           # Update organization
POST /api/admin/support/:id/verify    # Verify organization
DELETE /api/admin/support/:id         # Delete organization
GET  /api/admin/audit-logs            # View audit logs
```

---

## 💻 Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python wsgi.py
```

Backend runs on http://localhost:5000

### Frontend Development
```bash
cd frontend
npm start
```

Frontend runs on http://localhost:4200

### Database Setup
```bash
# Create indexes
python3 backend/scripts/setup_indexes.py

# Seed data
python3 backend/scripts/create_admin.py
```

### Environment Variables

Create `backend/.env`:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGODB_URI=mongodb://localhost:27017/homerights
OLLAMA_API_URL=http://localhost:11434
```

---

## 🐳 Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Deployment

#### Backend
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

#### Frontend
```bash
cd frontend
npm run build
# Serve dist/ folder with nginx or similar
```

#### MongoDB
```bash
mongod --dbpath /path/to/data/db
```

---

## 🔧 Troubleshooting

### Backend won't start
- Check MongoDB is running: `mongosh`
- Check Python version: `python3 --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify virtual environment is activated

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`
- Check port 4200 is free: `lsof -i :4200`

### Admin dashboard shows nothing
- Verify you're logged in as admin user
- Check backend is running on port 5001
- Check browser console for errors (F12)
- Re-run seed script: `python3 backend/scripts/create_admin.py`

### AI chat not working
- Check Ollama is installed: `ollama --version`
- Check Ollama is running: `curl http://localhost:11434/api/tags`
- Pull model: `ollama pull llama3.2`
- Start Ollama: `ollama serve`

### Database connection failed
- Check MongoDB is running: `mongosh`
- Check connection string in `.env`
- Check MongoDB port: `lsof -i :27017`
- Restart MongoDB service

### Can't upload documents
- Check `backend/uploads/` directory exists and is writable
- Check file size limit (default 10MB)
- Check file type (PDF only)
- Verify backend is running

**📖 For more detailed troubleshooting, see [SETUP.md](SETUP.md#troubleshooting)**

---

## 📊 Database Collections

### users
User accounts and profiles
```javascript
{
  email: String,
  passwordHash: String,
  role: String,  // user, super_admin, content_admin, support_admin, read_only
  profile: {
    firstName: String,
    lastName: String
  },
  savedItems: [ObjectId],
  createdAt: Date,
  lastLogin: Date
}
```

### topics
Housing law topics and articles
```javascript
{
  title: String,
  slug: String,
  category: String,  // eviction, deposits, repairs, rent, rights
  summary: String,
  body: String,
  tags: [String],
  published: Boolean,
  createdAt: Date,
  lastUpdated: Date,
  metadata: {
    views: Number,
    saves: Number,
    helpfulVotes: Number,
    notHelpfulVotes: Number
  }
}
```

### support_orgs
Support organizations
```javascript
{
  name: String,
  type: String,  // charity, advice_center, legal_aid, council
  description: String,
  services: [String],
  contact: {
    phone: String,
    email: String,
    website: String
  },
  address: String,
  location: {
    type: "Point",
    coordinates: [Number, Number]  // [longitude, latitude]
  },
  verificationStatus: String,  // verified, unverified, pending
  isAcceptingReferrals: Boolean,
  lastVerifiedAt: Date,
  createdAt: Date
}
```

### documents
Uploaded documents and analysis
```javascript
{
  userId: ObjectId,
  filename: String,
  filepath: String,
  filesize: Number,
  uploadedAt: Date,
  analysis: {
    riskLevel: String,  // critical, high, medium, low
    issues: [Object],
    summary: String
  }
}
```

### chat_messages
Chat conversation history
```javascript
{
  userId: ObjectId,
  sessionId: String,
  role: String,  // user, assistant
  content: String,
  timestamp: Date
}
```

### audit_logs
Admin action audit trail
```javascript
{
  adminId: ObjectId,
  adminEmail: String,
  action: String,
  targetEntity: String,
  targetId: String,
  before: Object,
  after: Object,
  ip: String,
  userAgent: String,
  timestamp: Date
}
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
cd frontend
npm run e2e
```

---

## 📝 Scripts

### Start/Stop
- `./start.sh` - Start all services (MongoDB, backend, frontend)
- `./stop.sh` - Stop all services

### Setup
- `python3 backend/scripts/create_admin.py` - Create admin user and seed data (15 topics, 15 organizations)
- `python3 backend/scripts/setup_indexes.py` - Create database indexes for performance

### Development
- `cd backend && source venv/bin/activate && python wsgi.py` - Run backend only
- `cd frontend && npm start` - Run frontend only
- `mongod --dbpath backend/data/db` - Run MongoDB only

---

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with detailed instructions and troubleshooting
- **[MVP_COMPLETE.md](MVP_COMPLETE.md)** - Full MVP documentation with architecture and features
- **[README.md](README.md)** - This file (project overview)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Team

Built with ❤️ for UK tenants

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@homerights.ai

---

## 🎯 Roadmap

### Phase 1 (Current - Completed ✅)
- ✅ User authentication and authorization
- ✅ Document upload and ML-powered analysis
- ✅ AI chat assistant using Ollama (Llama 3.2)
- ✅ Comprehensive housing law topics (15 topics)
- ✅ Support organization finder (15 organizations)
- ✅ Admin dashboard with full CRUD operations
- ✅ Role-based access control (5 roles)
- ✅ Audit logging for compliance

### Phase 2 (Planned - Q2 2026)
- [ ] Rich text editor for topic creation
- [ ] Email notifications for document analysis
- [ ] Advanced search with filters
- [ ] User feedback system
- [ ] Mobile-responsive improvements
- [ ] Performance optimizations

### Phase 3 (Future - Q3 2026)
- [ ] Mobile native apps (iOS/Android)
- [ ] Multi-language support (Welsh, Polish, Urdu)
- [ ] Video tutorial library
- [ ] Community forum
- [ ] Live chat support
- [ ] Advanced analytics dashboard

### Phase 4 (Long-term - Q4 2026)
- [ ] Integration with government APIs
- [ ] Automated legal document generation
- [ ] Machine learning model improvements
- [ ] API for third-party integrations
- [ ] Predictive analytics for housing disputes

---

**Last Updated**: March 2, 2026  
**Version**: 2.0.0  
**Status**: Production Ready ✅  
**Repository**: https://github.com/abdsayeed/Home-Rights.git

---

**Built with ❤️ for UK tenants**
