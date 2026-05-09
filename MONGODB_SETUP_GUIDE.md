# 🚀 Complete Setup Guide - MongoDB Version

Step-by-step guide to run the AI Chatbot with MongoDB on your local machine.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ **Node.js 18+** (for frontend)
- ✅ **Python 3.11+** (for backend)
- ✅ **MongoDB 6.0+** (database)
- ✅ **OpenRouter API key** ([Get one here](https://openrouter.ai/))

---

## 🗄️ STEP 1: Install & Start MongoDB

### Option A: Install MongoDB Locally (Recommended)

#### **macOS (using Homebrew)**

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community@7.0

# Start MongoDB service
brew services start mongodb-community@7.0

# Verify MongoDB is running
brew services list | grep mongodb

# Test connection
mongosh
# You should see: "Connecting to: mongodb://127.0.0.1:27017"
# Type "exit" to quit
```

#### **Windows**

1. Download MongoDB from: https://www.mongodb.com/try/download/community
2. Run the installer (choose "Complete" installation)
3. During installation, check "Install MongoDB as a Service"
4. MongoDB will start automatically
5. Verify by opening Command Prompt:
   ```cmd
   mongosh
   ```

#### **Linux (Ubuntu/Debian)**

```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Create list file
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update packages
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod

# Enable MongoDB to start on boot
sudo systemctl enable mongod

# Verify status
sudo systemctl status mongod

# Test connection
mongosh
```

### Option B: Use MongoDB Docker (Alternative)

```bash
# Pull MongoDB image
docker pull mongo:latest

# Run MongoDB container
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# Verify running
docker ps | grep mongodb

# Connect to MongoDB
docker exec -it mongodb mongosh
```

### Verify MongoDB is Running

```bash
# Check if MongoDB is accessible
mongosh --eval "db.adminCommand('ping')"

# Should output: { ok: 1 }
```

---

## ⚙️ STEP 2: Setup Backend (MongoDB Version)

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 2.3 Install Dependencies (MongoDB Version)

```bash
# Install MongoDB-specific dependencies
pip install -r requirements_mongodb.txt
```

**What's installed:**
- FastAPI (web framework)
- Motor (async MongoDB driver)
- Beanie (MongoDB ODM)
- PyMongo (MongoDB library)
- JWT authentication
- OpenRouter integration
- Testing tools

### 2.4 Configure Environment Variables

```bash
# Copy MongoDB example environment file
cp .env.mongodb.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Update the following in `.env`:**

```env
# MongoDB Connection (default local MongoDB)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=chatbot_db

# JWT Secret - Generate a secure random string
SECRET_KEY=your-super-secret-key-min-32-characters-long

# OpenRouter API Key - Get from https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# OpenRouter Model (choose one)
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# CORS - Frontend URL
CORS_ORIGINS=http://localhost:5173
```

**Generate Secure SECRET_KEY:**

```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(32))
# Copy the output to .env
```

### 2.5 Start Backend Server

```bash
# Make sure virtual environment is activated
# Run the MongoDB version of the app
uvicorn app.main_mongodb:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✅ Connected to MongoDB: chatbot_db
INFO:     Application startup complete.
```

### 2.6 Verify Backend

**Open browser and test:**

1. **API Root:** http://localhost:8000
   - Should show: `{"name": "AI Chatbot API", "version": "1.0.0", "database": "MongoDB", "status": "running"}`

2. **Health Check:** http://localhost:8000/health
   - Should show: `{"status": "healthy", "database": "MongoDB"}`

3. **API Documentation:** http://localhost:8000/docs
   - Interactive Swagger UI

4. **Alternative Docs:** http://localhost:8000/redoc
   - ReDoc documentation

---

## 🎨 STEP 3: Setup Frontend

### 3.1 Navigate to Frontend Directory

```bash
# Open new terminal (keep backend running)
cd frontend
```

### 3.2 Install Dependencies

```bash
# Install all frontend dependencies
npm install

# Install axios (for API calls)
npm install axios
```

### 3.3 Configure Environment (Optional)

```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

### 3.4 Update Frontend for API Integration

**Create `src/services/api.ts`:**

```bash
# Create services directory if it doesn't exist
mkdir -p src/services
```

Then create the file with this content:

```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle 401 errors
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

**Note:** For complete frontend integration, see `FRONTEND_INTEGRATION.md`

### 3.5 Start Frontend Development Server

```bash
npm run dev
```

**You should see:**

```
  VITE v7.3.2  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## ✅ STEP 4: Verify Everything Works

### 4.1 Check Services

**Terminal 1 (Backend):**
```
✅ Connected to MongoDB: chatbot_db
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 (Frontend):**
```
➜  Local: http://localhost:5173/
```

**MongoDB:**
```bash
# Check MongoDB is running
mongosh --eval "db.adminCommand('ping')"
# Should output: { ok: 1 }
```

### 4.2 Test Complete Flow

1. **Open Browser:** http://localhost:5173

2. **Sign Up:**
   - Click "Sign up"
   - Email: `test@example.com`
   - Password: `testpass123`
   - Name: `Test User`
   - Click "Sign Up"

3. **Verify Auto-Login:**
   - Should redirect to chat interface
   - First conversation auto-created

4. **Update Settings:**
   - Click "Settings" in sidebar
   - Choose role: "Developer"
   - Add context: "Building a web application with MongoDB"
   - Click "Save Changes"

5. **Send Message:**
   - Type: "Hello! Can you help me with MongoDB?"
   - Press Enter or click send
   - Wait for AI response

6. **Verify Response:**
   - Should receive context-aware response
   - Check if response mentions your role/context

### 4.3 Verify MongoDB Data

```bash
# Connect to MongoDB
mongosh

# Use chatbot database
use chatbot_db

# Check collections
show collections
# Should show: users, conversations, messages

# View users
db.users.find().pretty()

# View conversations
db.conversations.find().pretty()

# View messages
db.messages.find().pretty()

# Exit
exit
```

---

## 🐛 Troubleshooting

### Issue: MongoDB Connection Failed

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 61] Connection refused
```

**Solutions:**

1. **Check if MongoDB is running:**
   ```bash
   # macOS
   brew services list | grep mongodb
   brew services start mongodb-community@7.0
   
   # Linux
   sudo systemctl status mongod
   sudo systemctl start mongod
   
   # Windows - Check Services app
   ```

2. **Verify connection string in .env:**
   ```env
   MONGODB_URL=mongodb://localhost:27017
   ```

3. **Test MongoDB connection:**
   ```bash
   mongosh
   ```

---

### Issue: Backend Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'motor'
```

**Solution:**

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements_mongodb.txt
```

---

### Issue: OpenRouter API Error

**Error:**
```
OpenRouter API error: 401 Unauthorized
```

**Solutions:**

1. **Check API key in .env:**
   ```env
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key
   ```

2. **Verify key:**
   ```bash
   curl -H "Authorization: Bearer sk-or-v1-your-key" \
        https://openrouter.ai/api/v1/models
   ```

3. **Restart backend after changing .env**

---

### Issue: CORS Errors

**Error in browser:**
```
Access to fetch blocked by CORS policy
```

**Solution:**

1. **Update .env:**
   ```env
   CORS_ORIGINS=http://localhost:5173
   ```

2. **Restart backend server**

---

### Issue: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main_mongodb:app --port 8001
```

---

## 📊 MongoDB GUI Tools (Optional)

### MongoDB Compass (Official GUI)

1. **Download:** https://www.mongodb.com/try/download/compass
2. **Install** and open
3. **Connect:** `mongodb://localhost:27017`
4. **Browse** your `chatbot_db` database

### Studio 3T (Alternative)

1. **Download:** https://studio3t.com/download/
2. **Install** and open
3. **Connect** to localhost:27017
4. **View** collections and documents

---

## 🚀 Quick Commands Reference

### Start Everything

```bash
# Terminal 1 - MongoDB (if not running as service)
mongod

# Terminal 2 - Backend
cd backend
source venv/bin/activate
uvicorn app.main_mongodb:app --reload

# Terminal 3 - Frontend
cd frontend
npm run dev
```

### Stop Everything

```bash
# Stop backend: Ctrl+C in backend terminal
# Stop frontend: Ctrl+C in frontend terminal
# Stop MongoDB: 
brew services stop mongodb-community@7.0  # macOS
sudo systemctl stop mongod  # Linux
```

### View Logs

```bash
# MongoDB logs (macOS)
tail -f /usr/local/var/log/mongodb/mongo.log

# MongoDB logs (Linux)
sudo tail -f /var/log/mongodb/mongod.log

# Backend logs - in terminal running uvicorn
# Frontend logs - in browser console
```

---

## 📚 Next Steps

1. ✅ **Test all features:**
   - Create multiple conversations
   - Send messages with different roles
   - Update context and see AI adapt

2. ✅ **Explore MongoDB:**
   - Use MongoDB Compass to view data
   - Check indexes are created
   - View document structure

3. ✅ **Customize:**
   - Add new AI models
   - Modify role descriptions
   - Enhance UI

4. ✅ **Deploy:**
   - Use MongoDB Atlas (cloud MongoDB)
   - Deploy backend to Heroku/AWS
   - Deploy frontend to Vercel/Netlify

---

## 🎉 Success!

You now have a fully functional AI Chatbot running with:

- ✅ **Frontend** at http://localhost:5173
- ✅ **Backend API** at http://localhost:8000
- ✅ **MongoDB** storing all data
- ✅ **OpenRouter** powering AI responses

**Start chatting and enjoy!** 🤖💬

---

## 📝 MongoDB vs PostgreSQL

### Data Stored in MongoDB:

```javascript
// Users collection
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "name": "John Doe",
  "hashed_password": "...",
  "role_title": "Developer",
  "role_description": "Programming and technical help",
  "context": "Building web apps",
  "is_active": true,
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}

// Conversations collection
{
  "_id": ObjectId("..."),
  "user_id": "507f1f77bcf86cd799439011",
  "title": "Python Help",
  "message_count": 10,
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}

// Messages collection
{
  "_id": ObjectId("..."),
  "conversation_id": "507f1f77bcf86cd799439011",
  "content": "How do I use async/await?",
  "role": "user",
  "created_at": ISODate("...")
}
```

### Benefits of MongoDB:

- ✅ No schema migrations needed
- ✅ Flexible document structure
- ✅ Easy to scale horizontally
- ✅ JSON-like documents
- ✅ Fast for read-heavy workloads
- ✅ Great for rapid development

---

**For detailed API integration, see:** `FRONTEND_INTEGRATION.md`  
**For project context, see:** `PROJECT_CONTEXT.md`  
**For troubleshooting, see:** Above sections  

**Happy Coding with MongoDB!** 🚀
