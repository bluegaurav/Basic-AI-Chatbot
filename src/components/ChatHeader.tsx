import { Trash2, Bot, Menu } from 'lucide-react';

interface ChatHeaderProps {
  onClear: () => void;
  messageCount: number;
  onToggleSidebar?: () => void;
  userRole?: string;
}

export const ChatHeader = ({ onClear, messageCount, onToggleSidebar, userRole }: ChatHeaderProps) => {
  return (
    <div className="flex items-center justify-between px-4 sm:px-6 py-4 border-b border-gray-200 bg-white">
      <div className="flex items-center gap-3">
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            className="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Menu className="w-5 h-5 text-gray-600" />
          </button>
        )}
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center shadow-md">
          <Bot className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-semibold text-gray-900">AI Assistant</h1>
          <p className="text-xs text-gray-500">
            {userRole ? `Optimized for ${userRole}` : 'Always here to help'}
          </p>
        </div>
      </div>
      {messageCount > 0 && (
        <button
          onClick={onClear}
          className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          title="Clear chat"
        >
          <Trash2 className="w-4 h-4" />
          <span className="hidden sm:inline">Clear</span>
        </button>
      )}
    </div>
  );
};
