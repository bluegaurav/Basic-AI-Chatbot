# 🚀 AI Chatbot - Simple Setup Guide (MongoDB Only)

Complete guide to run the AI chatbot on your local machine.

---

## 📋 Step 1: Install Prerequisites

### A. Install Node.js
- Download from: https://nodejs.org/
- Install LTS version (18+)
- Verify: `node --version`

### B. Install Python
- Download from: https://python.org/downloads/
- Install Python 3.11+
- **Check "Add Python to PATH"**
- Verify: `python --version`

### C. Install MongoDB

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

**Windows:**
- Download: https://www.mongodb.com/try/download/community
- Run installer → Complete → Install as Service

**Linux:**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Verify MongoDB:**
```bash
mongosh
# Should connect successfully
# Type: exit
```

---

## ⚙️ Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Update `.env` file:**

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=chatbot_db

# Generate secret key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-generated-secret-key-here

# Get from https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

OPENROUTER_MODEL=openai/gpt-3.5-turbo
CORS_ORIGINS=http://localhost:5173
```

**Start backend:**
```bash
uvicorn app.main:app --reload
```

**✅ You should see:**
```
✅ Connected to MongoDB: chatbot_db
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Test:** Open http://localhost:8000 in browser

---

## 🎨 Step 3: Setup Frontend

**Open NEW terminal** (keep backend running)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Install axios
npm install axios

# Start frontend
npm run dev
```

**✅ You should see:**
```
➜ Local: http://localhost:5173/
```

---

## 🧪 Step 4: Test the Application

1. **Open browser:** http://localhost:5173

2. **Sign up:**
   - Email: test@example.com
   - Password: test123
   - Name: Test User

3. **Update settings:**
   - Click "Settings"
   - Choose role: "Developer"
   - Add context: "Learning web development"
   - Save

4. **Chat:**
   - Type: "Hello!"
   - Press Enter
   - Get AI response!

---

## 📁 Clean Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── conversations.py
│   │   │   └── messages.py
│   │   ├── deps.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   └── openrouter.py
│   └── main.py
├── requirements.txt
└── .env

frontend/
├── src/
│   ├── components/
│   ├── context/
│   ├── hooks/
│   ├── types/
│   ├── services/
│   │   └── api.ts  (create this)
│   └── App.tsx
└── package.json
```

---

## 🔧 Frontend API Integration

Create `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default api;
```

Then update `AuthContext.tsx`, `useChat.ts`, and `useConversations.ts` to use this API service (see `FRONTEND_INTEGRATION.md`).

---

## 🐛 Troubleshooting

### MongoDB not connecting?
```bash
# Check if running
mongosh

# Start MongoDB
# macOS:
brew services start mongodb-community@7.0
# Linux:
sudo systemctl start mongod
```

### Module not found?
```bash
# Backend:
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend:
cd frontend
npm install
```

### CORS error?
```bash
# Check backend/.env
CORS_ORIGINS=http://localhost:5173

# Restart backend
```

---

## 🎯 Quick Commands

**Start everything:**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

**Stop:**
- Press `Ctrl+C` in each terminal

---

## ✅ Verification Checklist

- [ ] MongoDB running (test with `mongosh`)
- [ ] Backend running (http://localhost:8000)
- [ ] Frontend running (http://localhost:5173)
- [ ] Can sign up
- [ ] Can login
- [ ] Can send messages
- [ ] Receive AI responses

---

## 📚 What's Different?

**✅ Removed:**
- All PostgreSQL code
- SQLAlchemy files
- Alembic migrations
- Duplicate MongoDB files (_mongodb suffix)

**✅ Optimized:**
- Clean imports
- Minimal code
- Single database (MongoDB only)
- Clear structure
- No redundancy

---

## 🎉 You're Done!

Your chatbot is now running with:
- ✅ MongoDB database
- ✅ Clean, minimal code
- ✅ FastAPI backend
- ✅ React frontend
- ✅ OpenRouter AI

**Start chatting!** 🤖

For detailed frontend integration, see `FRONTEND_INTEGRATION.md`
