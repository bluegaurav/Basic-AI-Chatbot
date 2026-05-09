# 📚 API Documentation

Complete API reference for the AI Chatbot backend.

---

## 🌐 Base URL

```
Development: http://localhost:8000/api
Production: https://api.yourdomain.com/api
```

---

## 🔐 Authentication

All protected endpoints require JWT token in header:

```
Authorization: Bearer <access_token>
```

---

## 📍 Endpoints

### **Authentication**

#### POST /auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": {
      "title": "General",
      "description": "General purpose assistance"
    },
    "context": null,
    "created_at": "2024-01-15T10:00:00Z"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Errors:**
- `400` - Email already registered
- `422` - Validation error

---

#### POST /auth/login
Login with email and password.

**Request:** `application/x-www-form-urlencoded`
```
username=user@example.com
password=securepass123
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": {
      "title": "Developer",
      "description": "Programming and technical help"
    },
    "context": "Working on FastAPI project",
    "created_at": "2024-01-15T10:00:00Z"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Errors:**
- `401` - Incorrect email or password

---

### **Users**

#### GET /users/me
Get current user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": {
    "title": "Developer",
    "description": "Programming and technical help"
  },
  "context": "Working on FastAPI project",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Errors:**
- `401` - Unauthorized

---

#### PUT /users/me
Update current user settings.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "name": "Jane Doe",
  "role_title": "Student",
  "role_description": "Learning and educational assistance",
  "context": "Studying Python and web development"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Jane Doe",
  "role": {
    "title": "Student",
    "description": "Learning and educational assistance"
  },
  "context": "Studying Python and web development",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Errors:**
- `401` - Unauthorized
- `422` - Validation error

---

### **Conversations**

#### GET /conversations/
List all conversations for current user.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int, optional) - Number of records to skip (default: 0)
- `limit` (int, optional) - Maximum number of records (default: 100)

**Response:** `200 OK`
```json
{
  "conversations": [
    {
      "id": 1,
      "title": "Python FastAPI Help",
      "message_count": 15,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T11:30:00Z"
    },
    {
      "id": 2,
      "title": "React State Management",
      "message_count": 8,
      "created_at": "2024-01-15T12:00:00Z",
      "updated_at": "2024-01-15T12:45:00Z"
    }
  ],
  "total": 2
}
```

---

#### POST /conversations/
Create a new conversation.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "My New Chat"
}
```

**Response:** `201 Created`
```json
{
  "id": 3,
  "title": "My New Chat",
  "message_count": 0,
  "created_at": "2024-01-15T13:00:00Z",
  "updated_at": "2024-01-15T13:00:00Z"
}
```

---

#### GET /conversations/{conversation_id}
Get conversation details.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Python FastAPI Help",
  "message_count": 15,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T11:30:00Z"
}
```

**Errors:**
- `404` - Conversation not found

---

#### PUT /conversations/{conversation_id}
Update conversation (e.g., change title).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "Updated Title"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Updated Title",
  "message_count": 15,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T14:00:00Z"
}
```

---

#### DELETE /conversations/{conversation_id}
Delete a conversation (and all its messages).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `204 No Content`

**Errors:**
- `404` - Conversation not found

---

#### DELETE /conversations/{conversation_id}/messages
Clear all messages from a conversation.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `204 No Content`

---

### **Messages**

#### GET /conversations/{conversation_id}/messages
Get all messages in a conversation.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int, optional) - Number of messages to skip
- `limit` (int, optional) - Maximum messages to return (default: 1000)

**Response:** `200 OK`
```json
{
  "messages": [
    {
      "id": 1,
      "content": "How do I create a FastAPI endpoint?",
      "role": "user",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "id": 2,
      "content": "Here's how to create a FastAPI endpoint...",
      "role": "assistant",
      "timestamp": "2024-01-15T10:00:05Z"
    }
  ],
  "total": 2
}
```

---

#### POST /conversations/{conversation_id}/chat
Send a chat message and get AI response.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "message": "Explain async/await in Python"
}
```

**Response:** `200 OK`
```json
{
  "user_message": {
    "id": 3,
    "content": "Explain async/await in Python",
    "role": "user",
    "timestamp": "2024-01-15T10:05:00Z"
  },
  "assistant_message": {
    "id": 4,
    "content": "Here's how you can implement this technically. Async/await in Python...",
    "role": "assistant",
    "timestamp": "2024-01-15T10:05:03Z"
  }
}
```

**Errors:**
- `404` - Conversation not found
- `500` - OpenRouter API error

**Note:** Response is context-aware based on user's role and custom context!

---

## 🔒 Error Responses

### Standard Error Format

```json
{
  "detail": "Error message here"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Successful, no body |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation failed |
| 500 | Internal Server Error - Server error |

---

## 📊 Data Models

### User Role

```typescript
{
  title: string;        // e.g., "Developer"
  description: string;  // e.g., "Programming and technical help"
}
```

**Available Roles:**
- Student
- Professional
- Developer
- Researcher
- Creative
- General

### User

```typescript
{
  id: number;
  email: string;
  name: string;
  role: UserRole;
  context: string | null;
  created_at: string;  // ISO 8601 datetime
}
```

### Conversation

```typescript
{
  id: number;
  title: string;
  message_count: number;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
}
```

### Message

```typescript
{
  id: number;
  content: string;
  role: "user" | "assistant";
  timestamp: string;  // ISO 8601 datetime
}
```

---

## 🧪 Example Workflow

### 1. Sign Up
```bash
POST /api/auth/signup
```

### 2. Create Conversation
```bash
POST /api/conversations/
```

### 3. Send Messages
```bash
POST /api/conversations/1/chat
```

### 4. Update Settings
```bash
PUT /api/users/me
```

### 5. Continue Chatting
```bash
POST /api/conversations/1/chat
# Now AI responses use updated role/context!
```

---

## 🔍 Testing with cURL

### Complete Flow Example

```bash
# 1. Sign up
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@test.com","password":"test123","name":"Dev User"}'

# Save token from response
TOKEN="your_access_token_here"

# 2. Create conversation
curl -X POST "http://localhost:8000/api/conversations/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"API Testing"}'

# 3. Send message
curl -X POST "http://localhost:8000/api/conversations/1/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello AI!"}'

# 4. Get messages
curl -X GET "http://localhost:8000/api/conversations/1/messages" \
  -H "Authorization: Bearer $TOKEN"

# 5. Update user settings
curl -X PUT "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Updated Name",
    "role_title":"Developer",
    "role_description":"Programming and technical help",
    "context":"Building a FastAPI application"
  }'

# 6. Send another message (will use updated context)
curl -X POST "http://localhost:8000/api/conversations/1/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"How do I optimize database queries?"}'
```

---

## 📝 Rate Limiting

Currently: **No rate limiting implemented**

To add rate limiting, install `slowapi`:

```bash
pip install slowapi
```

---

## 🔐 Security Considerations

### Password Requirements
- Minimum 6 characters
- Should include uppercase, lowercase, numbers, symbols (recommended)

### Token Expiration
- Default: 30 minutes
- Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`

### HTTPS
- **Required in production**
- Never send tokens over HTTP

---

## 📚 Additional Resources

- **Interactive Docs:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json
- **Alternative Docs:** http://localhost:8000/redoc

---

**Need more examples?** Check the test files in `tests/` directory!
