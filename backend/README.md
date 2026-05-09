# AI Chatbot API - FastAPI Backend

Production-ready FastAPI backend for AI Chatbot with OpenRouter integration.

## 🚀 Features

- ✅ **Authentication** - JWT-based auth with secure password hashing
- ✅ **User Management** - Profile, role, and context settings
- ✅ **Conversation Management** - Create, update, delete, list conversations
- ✅ **Message History** - Complete chat history persistence
- ✅ **OpenRouter Integration** - AI responses using OpenRouter API
- ✅ **Role-Based AI** - Context-aware responses based on user role
- ✅ **PostgreSQL Database** - Async SQLAlchemy with Alembic migrations
- ✅ **RESTful API** - Clean, organized endpoint structure
- ✅ **Test Coverage** - Comprehensive pytest test suite
- ✅ **Type Safety** - Full type hints with Pydantic
- ✅ **Security** - CORS, password hashing, JWT tokens
- ✅ **Scalable Architecture** - Modular, reusable code

## 📋 Requirements

- Python 3.11+
- PostgreSQL 14+
- OpenRouter API key

## 🛠️ Installation

### 1. Clone and Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/chatbot_db

# JWT
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# CORS
CORS_ORIGINS=http://localhost:5173
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb chatbot_db

# Database will be auto-created on first run
# Or use Alembic for migrations:
alembic upgrade head
```

## 🏃 Running the Server

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Create new account |
| POST | `/api/auth/login` | Login with credentials |
| POST | `/api/auth/token` | OAuth2 token endpoint |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me` | Get current user |
| PUT | `/api/users/me` | Update user settings |

### Conversations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/conversations/` | List all conversations |
| POST | `/api/conversations/` | Create conversation |
| GET | `/api/conversations/{id}` | Get conversation |
| PUT | `/api/conversations/{id}` | Update conversation |
| DELETE | `/api/conversations/{id}` | Delete conversation |
| DELETE | `/api/conversations/{id}/messages` | Clear messages |

### Messages

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/conversations/{id}/messages` | Get all messages |
| POST | `/api/conversations/{id}/chat` | Send message & get AI response |

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
```

### Test Results

All tests should pass:
- ✅ Authentication tests
- ✅ User management tests
- ✅ Conversation tests
- ✅ Message tests

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── users.py         # User management
│   │   │   ├── conversations.py # Conversation CRUD
│   │   │   └── messages.py      # Chat endpoints
│   │   └── api.py               # Router aggregation
│   ├── core/
│   │   ├── config.py            # Configuration
│   │   └── security.py          # JWT & password hashing
│   ├── crud/
│   │   ├── user.py              # User database operations
│   │   ├── conversation.py      # Conversation operations
│   │   └── message.py           # Message operations
│   ├── db/
│   │   ├── base.py              # Model imports
│   │   ├── base_class.py        # Base model class
│   │   └── session.py           # Database session
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── conversation.py      # Conversation model
│   │   └── message.py           # Message model
│   ├── schemas/
│   │   ├── user.py              # User Pydantic schemas
│   │   ├── conversation.py      # Conversation schemas
│   │   └── message.py           # Message schemas
│   ├── services/
│   │   └── openrouter.py        # OpenRouter AI service
│   └── main.py                  # FastAPI app
├── tests/
│   ├── conftest.py              # Test configuration
│   ├── test_auth.py             # Auth tests
│   ├── test_users.py            # User tests
│   ├── test_conversations.py   # Conversation tests
│   └── test_messages.py         # Message tests
├── .env.example                 # Environment template
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔑 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `SECRET_KEY` | JWT secret key | Random string |
| `OPENROUTER_API_KEY` | OpenRouter API key | Your API key |
| `OPENROUTER_MODEL` | AI model to use | `openai/gpt-3.5-turbo` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:5173` |

## 🔒 Security Features

- **Password Hashing** - Bcrypt with salt
- **JWT Tokens** - Secure token-based authentication
- **CORS Protection** - Configurable allowed origins
- **SQL Injection Prevention** - Parameterized queries
- **Input Validation** - Pydantic model validation
- **Rate Limiting** - (Add middleware if needed)

## 🎯 OpenRouter Integration

The API uses OpenRouter to connect to various AI models:

```python
# Supported models
- openai/gpt-3.5-turbo
- openai/gpt-4
- anthropic/claude-3-opus
- google/gemini-pro
# ... and more
```

### How It Works

1. User sends message
2. API retrieves conversation history
3. Builds context with user role & settings
4. Sends to OpenRouter API
5. Receives AI response
6. Saves both messages to database
7. Returns response to frontend

## 📊 Database Schema

### Users Table
```sql
- id (PK)
- email (unique)
- name
- hashed_password
- role_title
- role_description
- context
- is_active
- created_at
- updated_at
```

### Conversations Table
```sql
- id (PK)
- user_id (FK)
- title
- message_count
- created_at
- updated_at
```

### Messages Table
```sql
- id (PK)
- conversation_id (FK)
- content
- role (user/assistant)
- created_at
```

## 🚀 Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📈 Performance

- **Async/Await** - Non-blocking I/O
- **Connection Pooling** - SQLAlchemy pool
- **Efficient Queries** - Optimized with indexes
- **Caching** - (Add Redis if needed)

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### OpenRouter API Error

```bash
# Verify API key
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     https://openrouter.ai/api/v1/models
```

## 📝 License

This project is part of the AI Chatbot application.

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Add tests for new features
3. Update documentation
4. Run tests before committing

---

**Built with FastAPI, SQLAlchemy, and OpenRouter** 🚀
