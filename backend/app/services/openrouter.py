"""
OpenRouter AI service integration
"""
import httpx
from typing import List, Dict, Optional
from app.core.config import settings


class OpenRouterService:
    """Service for interacting with OpenRouter AI API"""
    
    def __init__(self):
        self.api_url = settings.OPENROUTER_API_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
    
    def _build_system_prompt(
        self,
        role_title: str,
        role_description: str,
        context: Optional[str] = None
    ) -> str:
        """Build system prompt based on user role and context"""
        prompt = f"You are an AI assistant helping a {role_title}. "
        prompt += f"Your role is to provide {role_description.lower()}. "
        
        if context:
            prompt += f"\n\nAdditional context about the user: {context}"
        
        prompt += "\n\nProvide helpful, accurate, and contextually relevant responses."
        return prompt
    
    def _build_messages(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        role_title: str,
        role_description: str,
        context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Build messages array for API request"""
        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt(
                    role_title,
                    role_description,
                    context
                )
            }
        ]
        
        # Add conversation history (last 10 messages for context)
        messages.extend(conversation_history[-10:])
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        role_title: str = "General",
        role_description: str = "General purpose assistance",
        context: Optional[str] = None
    ) -> str:
        """
        Generate AI response using OpenRouter API
        
        Args:
            user_message: The user's message
            conversation_history: Previous messages in conversation
            role_title: User's role title
            role_description: User's role description
            context: User's custom context
        
        Returns:
            AI-generated response text
        """
        messages = self._build_messages(
            user_message,
            conversation_history,
            role_title,
            role_description,
            context
        )
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Optional
            "X-Title": "AI Chatbot"  # Optional
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract response from OpenRouter format
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise ValueError("Invalid response format from OpenRouter")
                    
            except httpx.HTTPError as e:
                raise Exception(f"OpenRouter API error: {str(e)}")
            except Exception as e:
                raise Exception(f"Error generating AI response: {str(e)}")


# Global service instance
openrouter_service = OpenRouterService()
