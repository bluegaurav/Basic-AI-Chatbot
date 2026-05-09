import { useState, useCallback, useEffect } from 'react';
import api from '../lib/api';
import { Message, ChatState } from '../types/chat';
import { User } from '../types/user';

interface UseChatProps {
  user: User | null;
  conversationId: string | null;
  onMessagesChange?: (messages: Message[]) => void;
}

// Custom hook for managing chat logic
export const useChat = ({ user, conversationId, onMessagesChange }: UseChatProps) => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  const normalizeMessage = (message: any): Message => ({
    id: String(message.id),
    content: message.content,
    role: message.role,
    timestamp: new Date(message.timestamp),
  });

  useEffect(() => {
    if (!conversationId || !user) {
      setState((prev) => ({ ...prev, messages: [], error: null }));
      return;
    }

    let active = true;

    const loadMessages = async () => {
      try {
        const response = await api.get(`/conversations/${conversationId}/messages`);
        if (!active) return;

        setState((prev) => ({
          ...prev,
          messages: (response.data.messages || []).map(normalizeMessage),
          error: null,
        }));
      } catch {
        if (!active) return;
        setState((prev) => ({
          ...prev,
          messages: [],
          error: 'Failed to load messages.',
        }));
      }
    };

    void loadMessages();

    return () => {
      active = false;
    };
  }, [conversationId, user]);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || !conversationId || !user) return;

    const previousMessages = state.messages;
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
      const response = await api.post(`/conversations/${conversationId}/chat`, {
        message: content.trim(),
      });

      const responseData = response.data;
      const userReply = normalizeMessage(responseData.user_message);
      const assistantReply = normalizeMessage(responseData.assistant_message);
      const updatedMessages = [...previousMessages, userReply, assistantReply];

      setState(prev => ({
        ...prev,
        messages: updatedMessages,
        isLoading: false,
      }));

      onMessagesChange?.(updatedMessages);
    } catch (error) {
      setState(prev => ({
        ...prev,
        messages: previousMessages,
        isLoading: false,
        error: 'Failed to get response. Please try again.',
      }));
    }
  }, [conversationId, user, state.messages, onMessagesChange]);

  const clearChat = useCallback(() => {
    setState({
      messages: [],
      isLoading: false,
      error: null,
    });
  }, []);

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearChat,
  };
};
