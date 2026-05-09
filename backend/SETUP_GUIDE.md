# 🚀 Complete Setup Guide - FastAPI Backend

Step-by-step guide to set up and run the AI Chatbot API.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.11 or higher
- ✅ PostgreSQL 14 or higher
- ✅ pip (Python package manager)
- ✅ OpenRouter API key ([Get one here](https://openrouter.ai/))

---

## 🛠️ Step-by-Step Setup

### Step 1: Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Setup PostgreSQL Database

#### Option A: Using PostgreSQL Command Line

```bash
# Create database
createdb chatbot_db

# Or using psql
psql -U postgres
CREATE DATABASE chatbot_db;
\q
```

#### Option B: Using pgAdmin

1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `chatbot_db`
5. Click "Save"

### Step 3: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Update the following in `.env`:**

```env
# Database - Update with your credentials
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/chatbot_db

# JWT Secret - Generate a secure random string
SECRET_KEY=your-super-secret-key-min-32-characters-long

# OpenRouter API Key - Get from https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# CORS - Add your frontend URL
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Generate a secure SECRET_KEY:**

```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(32))
```

### Step 4: Initialize Database

The database tables will be created automatically when you start the server for the first time!

Alternatively, if you want to use Alembic migrations:

```bash
# Install alembic
pip install alembic

# Initialize alembic (already done)
# alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Step 5: Start the Development Server

```bash
# Make sure virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 6: Verify Installation

**Open your browser and visit:**

- API Root: http://localhost:8000/
- API Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

You should see the API documentation interface!

---

## 🧪 Running Tests

### Run All Tests

```bash
# Make sure you're in the backend directory with venv activated
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=html

# Open coverage report
# On macOS: open htmlcov/index.html
# On Linux: xdg-open htmlcov/index.html
# On Windows: start htmlcov/index.html
```

**Expected Test Results:**

```
tests/test_auth.py ................  [100%]
tests/test_conversations.py .......  [100%]
tests/test_messages.py .............  [100%]
tests/test_users.py ...............  [100%]

============ 40 passed in 2.5s ============
```

---

## 🔌 Testing API Endpoints

### Using Swagger UI (Recommended)

1. Go to http://localhost:8000/docs
2. Try the endpoints interactively
3. Click "Try it out" on any endpoint
4. Fill in parameters
5. Click "Execute"

### Using cURL

**1. Sign Up:**

```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test User"
  }'
```

**2. Login:**

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"
```

Save the `access_token` from the response!

**3. Get Current User:**

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**4. Create Conversation:**

```bash
curl -X POST "http://localhost:8000/api/conversations/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Chat"}'
```

**5. Send Chat Message:**

```bash
curl -X POST "http://localhost:8000/api/conversations/1/chat" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

### Using Postman/Insomnia

1. Import the API documentation from http://localhost:8000/openapi.json
2. Set up environment variables
3. Test all endpoints

---

## 🔧 Troubleshooting

### Issue: Database Connection Error

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**

1. **Check PostgreSQL is running:**
   ```bash
   # On macOS
   brew services list
   brew services start postgresql@14
   
   # On Linux
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   
   # On Windows
   # Check services.msc for PostgreSQL service
   ```

2. **Verify connection string:**
   ```bash
   # Test connection
   psql postgresql://postgres:password@localhost:5432/chatbot_db
   ```

3. **Check credentials in .env:**
   - Verify username, password, host, port

### Issue: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: OpenRouter API Errors

**Error:**
```
OpenRouter API error: 401 Unauthorized
```

**Solutions:**

1. **Verify API key:**
   - Check .env file has correct key
   - Verify key is active at https://openrouter.ai/
   
2. **Test API key:**
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" \
        https://openrouter.ai/api/v1/models
   ```

3. **Check credits:**
   - Ensure you have credits in OpenRouter account

### Issue: CORS Errors

**Error in frontend console:**
```
Access to fetch blocked by CORS policy
```

**Solution:**

1. **Update .env:**
   ```env
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```

2. **Restart server** after changing .env

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
uvicorn app.main:app --port 8001
```

### Issue: Test Failures

**Run tests in verbose mode:**

```bash
pytest -v -s
```

**Common issues:**
- Database not created (tests use in-memory SQLite)
- Missing dependencies: `pip install pytest pytest-asyncio`

---

## 📊 Database Management

### View Database Tables

```bash
psql -d chatbot_db

# List tables
\dt

# View users
SELECT * FROM user;

# View conversations
SELECT * FROM conversation;

# View messages
SELECT * FROM message;

# Exit
\q
```

### Reset Database

```bash
# Drop and recreate
dropdb chatbot_db
createdb chatbot_db

# Restart server (tables auto-create)
uvicorn app.main:app --reload
```

### Backup Database

```bash
pg_dump chatbot_db > backup.sql

# Restore
psql chatbot_db < backup.sql
```

---

## 🚀 Production Deployment

### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t chatbot-api .
docker run -p 8000:8000 --env-file .env chatbot-api
```

### Environment Variables for Production

```env
DEBUG=False
DATABASE_URL=postgresql+asyncpg://user:pass@production-db:5432/chatbot_db
SECRET_KEY=super-secure-production-key-64-characters-minimum
CORS_ORIGINS=https://your-frontend-domain.com
```

---

## 📈 Performance Tuning

### Database Connection Pool

Already configured in `app/db/session.py`:

```python
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections
    pool_size=10,        # Default connections
    max_overflow=20      # Extra connections
)
```

### Caching (Optional)

Add Redis for caching:

```bash
pip install redis aioredis
```

### Rate Limiting (Optional)

Add slowapi:

```bash
pip install slowapi
```

---

## ✅ Verification Checklist

Before going to production:

- [ ] All tests pass (`pytest`)
- [ ] Environment variables configured
- [ ] Database is PostgreSQL (not SQLite)
- [ ] SECRET_KEY is secure and unique
- [ ] CORS origins set correctly
- [ ] OpenRouter API key is valid
- [ ] API documentation accessible
- [ ] Health check endpoint works
- [ ] Gunicorn configured for production
- [ ] Database backups configured

---

## 🎉 Success!

If you've followed all steps, you should have:

✅ FastAPI server running on http://localhost:8000  
✅ PostgreSQL database connected  
✅ OpenRouter AI integration working  
✅ All tests passing  
✅ API documentation available  
✅ Ready to connect frontend  

---

## 📚 Next Steps

1. **Connect Frontend:**
   - Update frontend API URL
   - See `FRONTEND_INTEGRATION.md`

2. **Customize:**
   - Add more AI models
   - Implement features
   - Extend API

3. **Deploy:**
   - Choose hosting platform
   - Set up CI/CD
   - Configure monitoring

---

**Need help?** Check:
- API Docs: http://localhost:8000/docs
- README.md for detailed info
- FRONTEND_INTEGRATION.md for frontend setup

**Happy Coding!** 🚀
