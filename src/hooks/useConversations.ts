import { useState, useEffect, useCallback } from 'react';
import api from '../lib/api';
import { Conversation } from '../types/user';
import { Message } from '../types/chat';

export const useConversations = (userId: string | undefined) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  const normalizeConversation = (conversation: any): Conversation => ({
    id: String(conversation.id),
    userId: userId || '',
    title: conversation.title || 'New Conversation',
    createdAt: new Date(conversation.created_at || conversation.createdAt || Date.now()),
    updatedAt: new Date(conversation.updated_at || conversation.updatedAt || Date.now()),
    messageCount: conversation.message_count ?? conversation.messageCount ?? 0,
  });

  const refreshConversations = useCallback(async () => {
    if (!userId) {
      setConversations([]);
      setIsLoaded(true);
      return;
    }

    try {
      const response = await api.get('/conversations');
      const items = response.data.conversations || [];
      const normalized = items.map(normalizeConversation);
      setConversations(normalized);
      setIsLoaded(true);

      if (!currentConversationId && normalized.length > 0) {
        setCurrentConversationId(normalized[0].id);
      }
    } catch {
      setConversations([]);
      setIsLoaded(true);
    }
  }, [userId, currentConversationId]);

  useEffect(() => {
    setIsLoaded(false);
    void refreshConversations();
  }, [refreshConversations]);

  const createConversation = useCallback(async () => {
    if (!userId) return null;

    try {
      const response = await api.post('/conversations', {
        title: 'New Conversation',
      });
      const newConversation = normalizeConversation(response.data);
      setConversations((prev) => [newConversation, ...prev]);
      setCurrentConversationId(newConversation.id);
      return newConversation.id;
    } catch {
      return null;
    }
  }, [userId]);

  const deleteConversation = useCallback(
    async (conversationId: string) => {
      if (!userId) return;

      try {
        await api.delete(`/conversations/${conversationId}`);
        setConversations((prev) => prev.filter((c) => c.id !== conversationId));
        if (currentConversationId === conversationId) {
          setCurrentConversationId(null);
        }
      } catch {
        // Keep the current UI state if deletion fails.
      }
    },
    [userId, currentConversationId]
  );

  const updateConversationTitle = useCallback(
    async (conversationId: string, title: string) => {
      if (!userId) return;

      try {
        const response = await api.put(`/conversations/${conversationId}`, { title });
        const updatedConversation = normalizeConversation(response.data);
        setConversations((prev) =>
          prev.map((c) => (c.id === conversationId ? updatedConversation : c))
        );
      } catch {
        // Ignore backend failures and keep local state as-is.
      }
    },
    [userId]
  );

  const loadMessages = useCallback(async (conversationId: string): Promise<Message[]> => {
    if (!userId) return [];

    try {
      const response = await api.get(`/conversations/${conversationId}/messages`);
      return (response.data.messages || []).map((message: any) => ({
        id: String(message.id),
        content: message.content,
        role: message.role,
        timestamp: new Date(message.timestamp),
      }));
    } catch {
      return [];
    }
  }, [userId]);

  const saveMessages = useCallback(
    async (conversationId: string, messages: Message[]) => {
      if (!userId) return;

      if (messages.length === 0) {
        try {
          await api.delete(`/conversations/${conversationId}/messages`);
        } catch {
          // Ignore clear failures and let the UI continue.
        }
      }

      await refreshConversations();
    },
    [userId, refreshConversations]
  );

  return {
    conversations,
    currentConversationId,
    setCurrentConversationId,
    isLoaded,
    refreshConversations,
    createConversation,
    deleteConversation,
    updateConversationTitle,
    loadMessages,
    saveMessages,
  };
};
