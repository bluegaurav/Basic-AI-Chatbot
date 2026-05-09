import { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { TypingIndicator } from './TypingIndicator';
import { EmptyState } from './EmptyState';
import { Message } from '../types/chat';

interface ChatContainerProps {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

export const ChatContainer = ({ messages, isLoading, error }: ChatContainerProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  if (messages.length === 0) {
    return <EmptyState />;
  }

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 space-y-4"
    >
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message} />
      ))}
      
      {isLoading && <TypingIndicator />}
      
      {error && (
        <div className="flex justify-center">
          <div className="px-4 py-2 bg-red-50 border border-red-200 text-red-600 rounded-lg text-sm">
            {error}
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};
