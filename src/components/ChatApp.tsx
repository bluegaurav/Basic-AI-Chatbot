import { useState, useCallback } from 'react';
import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../hooks/useChat';
import { useConversations } from '../hooks/useConversations';
import { ChatHeader } from './ChatHeader';
import { ChatContainer } from './ChatContainer';
import { ChatInput } from './ChatInput';
import { Sidebar } from './Sidebar';
import { Settings } from './Settings';
import { Message } from '../types/chat';

export const ChatApp = () => {
  const { user, logout } = useAuth();
  const [showSettings, setShowSettings] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);

  const {
    conversations,
    currentConversationId,
    setCurrentConversationId,
    isLoaded,
    refreshConversations,
    createConversation,
    deleteConversation,
    saveMessages,
  } = useConversations(user?.id);

  const handleMessagesChange = useCallback(
    (messages: Message[]) => {
      if (currentConversationId) {
        saveMessages(currentConversationId, messages);
      }
    },
    [currentConversationId, saveMessages]
  );

  const { messages, isLoading, error, sendMessage, clearChat } = useChat({
    user,
    conversationId: currentConversationId,
    onMessagesChange: handleMessagesChange,
  });

  useEffect(() => {
    if (!user || !isLoaded) return;

    if (conversations.length > 0 && !currentConversationId) {
      setCurrentConversationId(conversations[0].id);
      return;
    }

    if (conversations.length === 0 && !currentConversationId) {
      void handleNewConversation();
    }
  }, [user, isLoaded, conversations, currentConversationId, setCurrentConversationId]);

  const handleNewConversation = async () => {
    const newId = await createConversation();
    if (newId) {
      setCurrentConversationId(newId);
    }
    setShowSidebar(false);
  };

  const handleSelectConversation = (id: string) => {
    setCurrentConversationId(id);
    setShowSidebar(false);
  };

  const handleDeleteConversation = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      await deleteConversation(id);
      await refreshConversations();
    }
  };

  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear this conversation?')) {
      clearChat();
      if (currentConversationId) {
        saveMessages(currentConversationId, []);
      }
    }
  };

  // Auto-create first conversation
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile Sidebar Overlay */}
      {showSidebar && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setShowSidebar(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed lg:static inset-y-0 left-0 z-50 transform transition-transform lg:transform-none ${
          showSidebar ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0`}
      >
        <Sidebar
          conversations={conversations}
          currentConversationId={currentConversationId}
          onSelectConversation={handleSelectConversation}
          onNewConversation={handleNewConversation}
          onDeleteConversation={handleDeleteConversation}
          onOpenSettings={() => setShowSettings(true)}
          onLogout={logout}
          userName={user?.name || ''}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="flex-1 flex flex-col bg-gradient-to-b from-gray-50 to-white overflow-hidden">
          {/* Header */}
          <ChatHeader
            onClear={handleClearChat}
            messageCount={messages.length}
            onToggleSidebar={() => setShowSidebar(!showSidebar)}
            userRole={user?.role?.title}
          />

          {/* Messages Container */}
          <ChatContainer messages={messages} isLoading={isLoading} error={error} />

          {/* Input Area */}
          <div className="px-4 sm:px-6 py-4 bg-white border-t border-gray-200">
            <ChatInput onSend={sendMessage} disabled={isLoading} />
          </div>
        </div>
      </div>

      {/* Settings Modal */}
      {showSettings && <Settings onClose={() => setShowSettings(false)} />}
    </div>
  );
};
