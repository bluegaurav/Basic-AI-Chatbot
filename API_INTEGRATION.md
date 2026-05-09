# 🔌 API Integration Guide

This guide shows you how to connect your AI chatbot frontend to various backend services.

## Quick Start

The main file to edit is `src/hooks/useChat.ts`. Replace the `generateAIResponse` function with your actual API call.

## Integration Examples

### 1. OpenAI API (ChatGPT)

```typescript
const generateAIResponse = async (userMessage: string): Promise<string> => {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant.'
        },
        {
          role: 'user',
          content: userMessage
        }
      ],
      temperature: 0.7,
      max_tokens: 500,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to get response from OpenAI');
  }

  const data = await response.json();
  return data.choices[0].message.content;
};
```

**Environment Variable** (create `.env` file):
```
VITE_OPENAI_API_KEY=sk-your-api-key-here
```

---

### 2. Custom Backend (Node.js/Express)

**Frontend (useChat.ts)**:
```typescript
const generateAIResponse = async (userMessage: string): Promise<string> => {
  const response = await fetch('http://localhost:3001/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: userMessage,
      conversationId: localStorage.getItem('conversationId'),
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to get response from server');
  }

  const data = await response.json();
  
  // Save conversation ID for context
  if (data.conversationId) {
    localStorage.setItem('conversationId', data.conversationId);
  }
  
  return data.response;
};
```

**Backend Example (Express)**:
```javascript
// server.js
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/chat', async (req, res) => {
  const { message, conversationId } = req.body;
  
  try {
    // Your AI logic here
    const aiResponse = await yourAIFunction(message, conversationId);
    
    res.json({
      response: aiResponse,
      conversationId: conversationId || generateNewId(),
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(3001, () => {
  console.log('Server running on port 3001');
});
```

---

### 3. Google Gemini API

```typescript
const generateAIResponse = async (userMessage: string): Promise<string> => {
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${import.meta.env.VITE_GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: userMessage
          }]
        }]
      }),
    }
  );

  if (!response.ok) {
    throw new Error('Failed to get response from Gemini');
  }

  const data = await response.json();
  return data.candidates[0].content.parts[0].text;
};
```

---

### 4. Anthropic Claude API

```typescript
const generateAIResponse = async (userMessage: string): Promise<string> => {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': import.meta.env.VITE_ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-3-sonnet-20240229',
      max_tokens: 1024,
      messages: [{
        role: 'user',
        content: userMessage
      }]
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to get response from Claude');
  }

  const data = await response.json();
  return data.content[0].text;
};
```

---

### 5. Hugging Face Inference API

```typescript
const generateAIResponse = async (userMessage: string): Promise<string> => {
  const response = await fetch(
    'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${import.meta.env.VITE_HF_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        inputs: userMessage,
      }),
    }
  );

  if (!response.ok) {
    throw new Error('Failed to get response from Hugging Face');
  }

  const data = await response.json();
  return data[0].generated_text;
};
```

---

### 6. Local LLM (Ollama)

```typescript
const generateAIResponse = async (userMessage: string): Promise<string> => {
  const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'llama2',
      prompt: userMessage,
      stream: false,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to get response from Ollama');
  }

  const data = await response.json();
  return data.response;
};
```

---

## Advanced Features

### 1. Streaming Responses

For real-time token streaming (like ChatGPT):

```typescript
const sendMessage = useCallback(async (content: string) => {
  if (!content.trim()) return;

  const userMessage: Message = {
    id: Date.now().toString(),
    content: content.trim(),
    role: 'user',
    timestamp: new Date(),
  };

  setState(prev => ({
    ...prev,
    messages: [...prev.messages, userMessage],
    isLoading: true,
    error: null,
  }));

  try {
    const response = await fetch('YOUR_API_ENDPOINT', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: content }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let aiMessageContent = '';

    const aiMessageId = (Date.now() + 1).toString();
    
    // Add empty AI message
    setState(prev => ({
      ...prev,
      messages: [
        ...prev.messages,
        {
          id: aiMessageId,
          content: '',
          role: 'assistant',
          timestamp: new Date(),
        },
      ],
    }));

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value);
      aiMessageContent += chunk;

      // Update the AI message with new content
      setState(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === aiMessageId
            ? { ...msg, content: aiMessageContent }
            : msg
        ),
      }));
    }

    setState(prev => ({ ...prev, isLoading: false }));
  } catch (error) {
    setState(prev => ({
      ...prev,
      isLoading: false,
      error: 'Failed to get response',
    }));
  }
}, []);
```

### 2. Conversation Context

To maintain conversation history:

```typescript
// In useChat.ts
const generateAIResponse = async (
  userMessage: string,
  conversationHistory: Message[]
): Promise<string> => {
  const messages = conversationHistory.map(msg => ({
    role: msg.role === 'user' ? 'user' : 'assistant',
    content: msg.content,
  }));

  messages.push({
    role: 'user',
    content: userMessage,
  });

  const response = await fetch('YOUR_API_ENDPOINT', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });

  // ... rest of the code
};

// Update sendMessage to pass conversation history
const responseContent = await generateAIResponse(content, state.messages);
```

### 3. Error Handling with Retry

```typescript
const generateAIResponse = async (
  userMessage: string,
  retries = 3
): Promise<string> => {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch('YOUR_API_ENDPOINT', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.response;
    } catch (error) {
      if (i === retries - 1) throw error;
      // Wait before retrying (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
  throw new Error('Max retries reached');
};
```

### 4. Request Cancellation

```typescript
// In useChat.ts
const abortControllerRef = useRef<AbortController | null>(null);

const sendMessage = useCallback(async (content: string) => {
  // Cancel previous request if still pending
  if (abortControllerRef.current) {
    abortControllerRef.current.abort();
  }

  abortControllerRef.current = new AbortController();

  try {
    const response = await fetch('YOUR_API_ENDPOINT', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: content }),
      signal: abortControllerRef.current.signal,
    });

    // ... rest of the code
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Request cancelled');
      return;
    }
    // Handle other errors
  }
}, []);
```

## Environment Variables Setup

Create a `.env` file in your project root:

```env
# OpenAI
VITE_OPENAI_API_KEY=sk-your-key-here

# Gemini
VITE_GEMINI_API_KEY=your-key-here

# Anthropic
VITE_ANTHROPIC_API_KEY=your-key-here

# Hugging Face
VITE_HF_API_KEY=your-key-here

# Custom Backend
VITE_API_BASE_URL=http://localhost:3001
```

**Important**: Add `.env` to your `.gitignore` file!

## Security Best Practices

1. **Never expose API keys in frontend code**
   - Use environment variables
   - Consider using a proxy backend

2. **Use a Backend Proxy** (Recommended)
   ```
   Frontend -> Your Backend -> AI API
   ```
   This keeps API keys secure on the server

3. **Implement Rate Limiting**
   - Prevent abuse
   - Track usage per user

4. **Validate User Input**
   - Sanitize messages
   - Check message length
   - Prevent injection attacks

5. **Use HTTPS**
   - Always use secure connections
   - Enable CORS properly

## Testing Your Integration

1. **Test Error Cases**:
   - Network errors
   - API errors
   - Invalid responses
   - Timeout scenarios

2. **Test Edge Cases**:
   - Very long messages
   - Special characters
   - Empty responses
   - Rapid successive messages

3. **Performance Testing**:
   - Response times
   - Loading states
   - Memory usage
   - Bundle size

## Troubleshooting

### CORS Issues
If you get CORS errors, you need to either:
- Configure your backend to allow requests from your frontend domain
- Use a proxy server
- Use a serverless function as a proxy

### API Key Not Working
- Check if the environment variable is properly prefixed with `VITE_`
- Restart the dev server after adding environment variables
- Verify the API key is valid and has proper permissions

### No Response
- Check browser console for errors
- Verify API endpoint is correct
- Check network tab in dev tools
- Ensure API key has sufficient credits/quota

---

**Ready to connect your AI backend!** 🚀
