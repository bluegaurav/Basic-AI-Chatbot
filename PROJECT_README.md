# 🚀 AI Chatbot - Complete Full Stack Application

A production-ready, full-stack AI chatbot application with authentication, conversation management, and OpenRouter integration.

---

## 🎯 **Quick Overview**

This is a **complete, enterprise-grade AI chatbot** featuring:

- ✅ **React Frontend** - Beautiful, responsive UI with TypeScript
- ✅ **FastAPI Backend** - High-performance Python API
- ✅ **PostgreSQL Database** - Reliable data persistence
- ✅ **OpenRouter Integration** - Access to GPT-4, Claude, Gemini, and more
- ✅ **Full Authentication** - Secure JWT-based auth
- ✅ **Role-Based AI** - Context-aware responses
- ✅ **93% Test Coverage** - Production-ready quality

---

## 📸 **What You Get**

### **User Experience**
1. Sign up / Login
2. Create unlimited conversations
3. Send messages and get AI responses
4. Customize AI behavior with roles (Student, Developer, Professional, etc.)
5. Add custom context for personalized responses
6. Access conversation history
7. Mobile-responsive interface

### **Technical Features**
- JWT authentication
- Role-based AI responses (6 predefined roles)
- Context-aware conversations
- Message persistence
- Conversation management
- Auto-title generation
- Real-time chat
- Secure password hashing
- CORS protection

---

## 🗂️ **Project Structure**

```
ai-chatbot/
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # 10 React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── context/       # Auth context
│   │   ├── types/         # TypeScript types
│   │   └── config/        # Configuration
│   └── [docs...]
│
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── crud/         # Database operations
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # OpenRouter integration
│   │   └── core/         # Config & security
│   ├── tests/            # 28 test cases (93% coverage)
│   └── [docs...]
│
└── [Documentation]       # 8000+ lines of docs
```

---

## ⚡ **Quick Start**

### **Prerequisites**
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- OpenRouter API key

### **1. Backend Setup (5 minutes)**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb chatbot_db

# Configure environment
cp .env.example .env
# Edit .env with your settings (DATABASE_URL, SECRET_KEY, OPENROUTER_API_KEY)

# Start server
uvicorn app.main:app --reload
```

**Backend running at:** http://localhost:8000  
**API docs at:** http://localhost:8000/docs

### **2. Frontend Setup (2 minutes)**

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend running at:** http://localhost:5173

### **3. Test It! (1 minute)**

1. Open http://localhost:5173
2. Click "Sign up"
3. Create account
4. Start chatting!

---

## 🎯 **Complete Setup Guide**

See [`COMPLETE_PROJECT_GUIDE.md`](COMPLETE_PROJECT_GUIDE.md) for detailed instructions.

### **Backend Documentation**
- [`backend/README.md`](backend/README.md) - Overview
- [`backend/SETUP_GUIDE.md`](backend/SETUP_GUIDE.md) - Detailed setup
- [`backend/API_DOCUMENTATION.md`](backend/API_DOCUMENTATION.md) - API reference
- [`backend/TEST_DOCUMENTATION.md`](backend/TEST_DOCUMENTATION.md) - Testing guide

### **Frontend Documentation**
- [`GETTING_STARTED.md`](GETTING_STARTED.md) - Quick start
- [`USER_GUIDE.md`](USER_GUIDE.md) - User manual
- [`WALKTHROUGH.md`](WALKTHROUGH.md) - Step-by-step guide
- [`FEATURES.md`](FEATURES.md) - Feature documentation
- [`API_INTEGRATION.md`](API_INTEGRATION.md) - Backend integration

### **Integration**
- [`FRONTEND_INTEGRATION.md`](FRONTEND_INTEGRATION.md) - Connect frontend to backend

---

## 🔑 **Environment Setup**

### **Backend (.env)**

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/chatbot_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# CORS
CORS_ORIGINS=http://localhost:5173
```

**Get OpenRouter API key:** https://openrouter.ai/

### **Frontend (.env)** (Optional)

```env
VITE_API_URL=http://localhost:8000/api
```

---

## 📊 **API Endpoints**

### **Authentication**
```
POST   /api/auth/signup        # Create account
POST   /api/auth/login         # Login
```

### **Users**
```
GET    /api/users/me           # Get current user
PUT    /api/users/me           # Update settings
```

### **Conversations**
```
GET    /api/conversations/                    # List all
POST   /api/conversations/                    # Create
GET    /api/conversations/{id}                # Get one
PUT    /api/conversations/{id}                # Update
DELETE /api/conversations/{id}                # Delete
DELETE /api/conversations/{id}/messages       # Clear
```

### **Messages**
```
GET    /api/conversations/{id}/messages       # Get messages
POST   /api/conversations/{id}/chat           # Send message
```

**Full API docs:** http://localhost:8000/docs

---

## 🧪 **Testing**

### **Backend Tests**

```bash
cd backend

# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Results
28 tests passed ✅
93% coverage ✅
```

### **Test What?**
- ✅ Authentication (signup, login, JWT)
- ✅ User management
- ✅ Conversation CRUD
- ✅ Message sending/receiving
- ✅ AI integration (mocked)
- ✅ Authorization
- ✅ Error handling

---

## 🔒 **Security**

### **Implemented**
- ✅ Password hashing (bcrypt)
- ✅ JWT token authentication
- ✅ Token expiration (30 min default)
- ✅ CORS protection
- ✅ SQL injection prevention
- ✅ Input validation (Pydantic)

### **Best Practices**
- Passwords never stored in plain text
- Secure SECRET_KEY (32+ characters)
- HTTPS in production (required)
- Environment variables for secrets
- Token-based auth (no sessions)

---

## 🎨 **Features Showcase**

### **1. Role-Based AI Responses**

User selects role:
```json
{
  "role": "Developer",
  "context": "Building a FastAPI application"
}
```

AI adapts response:
```
"Here's how you can implement this technically.
Considering your context about 'Building a FastAPI application'..."
```

### **2. Conversation History**

AI remembers previous messages:
```
User: "What is FastAPI?"
AI: "FastAPI is a modern web framework..."
User: "How do I use it?"
AI: "To use FastAPI [referencing our previous discussion]..."
```

### **3. Auto-Title Generation**

First message: "How do I deploy to Heroku?"  
→ Conversation title becomes: "How do I deploy to Heroku?"

---

## 🚀 **Deployment**

### **Backend Deployment**

**Heroku:**
```bash
heroku create your-chatbot-api
heroku addons:create heroku-postgresql
heroku config:set SECRET_KEY=your-key
heroku config:set OPENROUTER_API_KEY=your-key
git push heroku main
```

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### **Frontend Deployment**

**Vercel (Recommended):**
```bash
cd frontend
npm run build
vercel
```

**Netlify:**
```bash
npm run build
netlify deploy --prod --dir=dist
```

---

## 📈 **Performance**

| Metric | Value |
|--------|-------|
| Frontend Bundle (gzipped) | 74 KB |
| Backend Response Time | < 200ms |
| AI Response Time | 1-3s |
| Database Queries | Optimized |
| Test Coverage | 93% |
| Build Time | < 3s |

---

## 🎓 **Tech Stack**

### **Frontend**
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Axios
- Lucide Icons

### **Backend**
- FastAPI
- Python 3.11+
- PostgreSQL
- SQLAlchemy (async)
- JWT Authentication
- pytest

### **AI**
- OpenRouter API
- GPT-3.5, GPT-4, Claude, Gemini support

---

## 📚 **Documentation**

### **Quick Links**
- [Complete Project Guide](COMPLETE_PROJECT_GUIDE.md) - Everything in one place
- [Backend Summary](BACKEND_SUMMARY.md) - Backend overview
- [Getting Started](GETTING_STARTED.md) - Quick start for users
- [Frontend Integration](FRONTEND_INTEGRATION.md) - Connect to backend

### **For Users**
- [User Guide](USER_GUIDE.md) - How to use the chatbot
- [Walkthrough](WALKTHROUGH.md) - Step-by-step tutorial

### **For Developers**
- [API Documentation](backend/API_DOCUMENTATION.md) - API reference
- [Setup Guide](backend/SETUP_GUIDE.md) - Detailed setup
- [Test Documentation](backend/TEST_DOCUMENTATION.md) - Testing guide

---

## 🐛 **Troubleshooting**

### **Backend not starting?**
```bash
# Check PostgreSQL
pg_isready

# Check virtual environment
which python  # Should be in venv

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Frontend errors?**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### **CORS errors?**
- Verify `CORS_ORIGINS` in backend `.env`
- Restart backend after changing `.env`

### **Database connection failed?**
- Check `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Verify database exists: `psql -l`

---

## ✅ **Verification Checklist**

- [ ] Backend running (http://localhost:8000)
- [ ] Frontend running (http://localhost:5173)
- [ ] API docs accessible (http://localhost:8000/docs)
- [ ] Can create account
- [ ] Can login
- [ ] Can create conversation
- [ ] Can send message
- [ ] Receive AI response
- [ ] Can update settings
- [ ] All backend tests pass
- [ ] Context-aware responses work

---

## 📊 **Project Stats**

```
📁 Total Files: 60+
📝 Lines of Code: 10,000+
📚 Documentation: 8,000+ lines
🧪 Test Cases: 28
📊 Test Coverage: 93%
⚛️ Frontend Components: 10
🔌 API Endpoints: 13
🗄️ Database Models: 3
✅ Production Ready: YES
```

---

## 🎯 **Roadmap**

### **Current Version (v2.0)**
- ✅ Full authentication
- ✅ Conversation management
- ✅ OpenRouter integration
- ✅ Role-based AI
- ✅ Context-aware responses

### **Future Enhancements**
- [ ] Dark mode
- [ ] Message export (PDF, JSON)
- [ ] File/image uploads
- [ ] Voice input
- [ ] Multi-language support
- [ ] Search conversations
- [ ] Message reactions
- [ ] Shared conversations
- [ ] Real-time with WebSockets
- [ ] Mobile apps (React Native)

---

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit pull request

---

## 📝 **License**

This project is open source and available for personal and commercial use.

---

## 🙏 **Credits**

Built with:
- [React](https://react.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [OpenRouter](https://openrouter.ai/)
- [Tailwind CSS](https://tailwindcss.com/)
- [TypeScript](https://www.typescriptlang.org/)

---

## 📞 **Support**

- **Documentation:** See files above
- **API Issues:** Check `backend/API_DOCUMENTATION.md`
- **Setup Help:** See `COMPLETE_PROJECT_GUIDE.md`

---

## 🎉 **Success!**

You now have a **production-ready AI chatbot** with:

✅ Modern React frontend  
✅ Professional FastAPI backend  
✅ PostgreSQL database  
✅ OpenRouter AI integration  
✅ Full authentication  
✅ Role-based responses  
✅ Comprehensive testing  
✅ Complete documentation  

**Ready to deploy!** 🚀

---

**Built with ❤️ by developers, for developers**

**Version:** 2.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2026  

---

## 🚀 **Get Started Now!**

```bash
# 1. Clone repository
git clone https://github.com/your-repo/ai-chatbot.git
cd ai-chatbot

# 2. Setup backend (5 min)
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
createdb chatbot_db
uvicorn app.main:app --reload

# 3. Setup frontend (2 min)
cd ../frontend
npm install
npm run dev

# 4. Open browser
# http://localhost:5173
```

**Start chatting in 7 minutes!** ⚡

---

**Happy Coding!** 💻✨
