```markdown
# 🔌 Frontend Integration Guide

How to connect your React frontend to the FastAPI backend.

---

## 🎯 Overview

The backend API is now ready. Follow these steps to integrate it with your React frontend.

---

## 📝 Step 1: Update Frontend API Configuration

### Create API Service File

Create `src/services/api.ts`:

```typescript
// src/services/api.ts
import axios from 'axios';

// API Base URL - Update based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
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

// Handle 401 errors (logout)
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

---

## 📝 Step 2: Update Authentication Context

Update `src/context/AuthContext.tsx`:

```typescript
import api from '../services/api';

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);

  const signup = async (
    email: string,
    password: string,
    name: string
  ): Promise<boolean> => {
    try {
      const response = await api.post('/auth/signup', {
        email,
        password,
        name,
      });

      const { user: userData, access_token } = response.data;
      
      setUser(userData);
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return true;
    } catch (error) {
      console.error('Signup error:', error);
      return false;
    }
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const { user: userData, access_token } = response.data;
      
      setUser(userData);
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  };

  const updateUser = async (userData: Partial<User>) => {
    try {
      const response = await api.put('/users/me', userData);
      setUser(response.data);
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch (error) {
      console.error('Update user error:', error);
    }
  };

  // Load user on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, updateUser, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};
```

---

## 📝 Step 3: Update Conversations Hook

Update `src/hooks/useConversations.ts`:

```typescript
import api from '../services/api';

export const useConversations = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);

  // Load conversations from API
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const response = await api.get('/conversations/');
      setConversations(response.data.conversations);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const createConversation = async () => {
    try {
      const response = await api.post('/conversations/', {
        title: 'New Conversation',
      });
      
      const newConv = response.data;
      setConversations([newConv, ...conversations]);
      setCurrentConversationId(newConv.id.toString());
      return newConv.id.toString();
    } catch (error) {
      console.error('Error creating conversation:', error);
      return null;
    }
  };

  const deleteConversation = async (conversationId: string) => {
    try {
      await api.delete(`/conversations/${conversationId}`);
      setConversations(conversations.filter((c) => c.id !== parseInt(conversationId)));
      
      if (currentConversationId === conversationId) {
        setCurrentConversationId(null);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const updateConversationTitle = async (conversationId: string, title: string) => {
    try {
      await api.put(`/conversations/${conversationId}`, { title });
      setConversations(
        conversations.map((c) =>
          c.id === parseInt(conversationId) ? { ...c, title } : c
        )
      );
    } catch (error) {
      console.error('Error updating conversation:', error);
    }
  };

  const loadMessages = async (conversationId: string): Promise<Message[]> => {
    try {
      const response = await api.get(`/conversations/${conversationId}/messages`);
      return response.data.messages;
    } catch (error) {
      console.error('Error loading messages:', error);
      return [];
    }
  };

  return {
    conversations,
    currentConversationId,
    setCurrentConversationId,
    createConversation,
    deleteConversation,
    updateConversationTitle,
    loadMessages,
    loadConversations,
  };
};
```

---

## 📝 Step 4: Update Chat Hook

Update `src/hooks/useChat.ts`:

```typescript
import api from '../services/api';

export const useChat = ({ user, conversationId, onMessagesChange }: UseChatProps) => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  // Load messages when conversation changes
  useEffect(() => {
    if (conversationId) {
      loadMessages();
    } else {
      setState((prev) => ({ ...prev, messages: [] }));
    }
  }, [conversationId]);

  const loadMessages = async () => {
    if (!conversationId) return;
    
    try {
      const response = await api.get(`/conversations/${conversationId}/messages`);
      setState((prev) => ({
        ...prev,
        messages: response.data.messages.map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp),
        })),
      }));
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || !conversationId) return;

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await api.post(`/conversations/${conversationId}/chat`, {
        message: content,
      });

      const { user_message, assistant_message } = response.data;

      const newMessages = [
        {
          id: user_message.id,
          content: user_message.content,
          role: user_message.role,
          timestamp: new Date(user_message.timestamp),
        },
        {
          id: assistant_message.id,
          content: assistant_message.content,
          role: assistant_message.role,
          timestamp: new Date(assistant_message.timestamp),
        },
      ];

      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, ...newMessages],
        isLoading: false,
      }));

      onMessagesChange?.(newMessages);
    } catch (error: any) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error.response?.data?.detail || 'Failed to get response',
      }));
    }
  }, [conversationId, onMessagesChange]);

  const clearChat = async () => {
    if (!conversationId) return;

    try {
      await api.delete(`/conversations/${conversationId}/messages`);
      setState((prev) => ({ ...prev, messages: [] }));
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearChat,
  };
};
```

---

## 📝 Step 5: Environment Variables

Create `.env` in frontend root:

```env
# API URL
VITE_API_URL=http://localhost:8000/api

# For production
# VITE_API_URL=https://api.yourdomain.com/api
```

---

## 📝 Step 6: Install Axios

```bash
cd frontend
npm install axios
```

---

## 🧪 Step 7: Test Integration

### 1. Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

### 3. Test Flow

1. **Sign up** - Create new account
2. **Login** - Login with credentials
3. **Create conversation** - Click "New Chat"
4. **Send message** - Type and send
5. **Receive AI response** - Wait for OpenRouter response
6. **Check settings** - Update role and context
7. **Send another message** - Verify context-aware response

---

## 🔍 Debugging Tips

### Check Network Requests

Open browser DevTools → Network tab:

1. **Signup/Login** - Check request/response
2. **Conversations** - Verify API calls
3. **Chat** - Monitor message sending

### Common Issues

**401 Unauthorized:**
- Token expired or invalid
- Check localStorage for `access_token`
- Login again

**CORS Errors:**
- Verify backend CORS settings
- Check `.env` CORS_ORIGINS

**Network Errors:**
- Backend not running
- Wrong API URL
- Firewall blocking

---

## 📊 API Response Format Reference

### Signup/Login Response
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "User Name",
    "role": {
      "title": "General",
      "description": "General purpose assistance"
    },
    "context": null,
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Conversations List Response
```json
{
  "conversations": [
    {
      "id": 1,
      "title": "My First Chat",
      "message_count": 10,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T01:00:00"
    }
  ],
  "total": 1
}
```

### Chat Response
```json
{
  "user_message": {
    "id": 1,
    "content": "Hello!",
    "role": "user",
    "timestamp": "2024-01-01T00:00:00"
  },
  "assistant_message": {
    "id": 2,
    "content": "Hi! How can I help you today?",
    "role": "assistant",
    "timestamp": "2024-01-01T00:00:01"
  }
}
```

---

## ✅ Integration Checklist

- [ ] Axios installed
- [ ] API service created
- [ ] AuthContext updated
- [ ] useConversations updated
- [ ] useChat updated
- [ ] Environment variables set
- [ ] Backend running
- [ ] Frontend running
- [ ] Signup works
- [ ] Login works
- [ ] Conversations load
- [ ] Messages send/receive
- [ ] Settings update
- [ ] AI responses working

---

## 🎉 Success!

Your frontend is now fully integrated with the FastAPI backend!

**Test the full flow:**
1. Create account ✅
2. Login ✅
3. Create conversation ✅
4. Send message ✅
5. Get AI response ✅
6. Update settings ✅
7. Context-aware responses ✅

---

**Next:** Deploy both frontend and backend to production!
```
