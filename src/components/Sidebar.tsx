import { MessageSquare, Plus, Trash2, Settings as SettingsIcon, LogOut } from 'lucide-react';
import { Conversation } from '../types/user';

interface SidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
  onDeleteConversation: (id: string) => void;
  onOpenSettings: () => void;
  onLogout: () => void;
  userName: string;
}

export const Sidebar = ({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  onOpenSettings,
  onLogout,
  userName,
}: SidebarProps) => {
  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <button
          onClick={onNewConversation}
          className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
        >
          <Plus className="w-5 h-5" />
          New Chat
        </button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {conversations.length === 0 ? (
          <div className="text-gray-400 text-sm text-center py-8">
            No conversations yet
          </div>
        ) : (
          conversations
            .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())
            .map((conv) => (
              <div
                key={conv.id}
                className={`group relative rounded-lg transition-colors ${
                  currentConversationId === conv.id
                    ? 'bg-gray-800'
                    : 'hover:bg-gray-800'
                }`}
              >
                <button
                  onClick={() => onSelectConversation(conv.id)}
                  className="w-full text-left p-3 pr-10"
                >
                  <div className="flex items-start gap-3">
                    <MessageSquare className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium truncate">
                        {conv.title}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {conv.messageCount} messages
                      </div>
                    </div>
                  </div>
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteConversation(conv.id);
                  }}
                  className="absolute right-2 top-3 p-1.5 opacity-0 group-hover:opacity-100 hover:bg-red-600 rounded transition-all"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800 space-y-2">
        <button
          onClick={onOpenSettings}
          className="w-full py-2.5 px-4 hover:bg-gray-800 rounded-lg transition-colors flex items-center gap-3 text-sm"
        >
          <SettingsIcon className="w-4 h-4" />
          Settings
        </button>
        <button
          onClick={onLogout}
          className="w-full py-2.5 px-4 hover:bg-gray-800 rounded-lg transition-colors flex items-center gap-3 text-sm text-red-400"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
        <div className="pt-2 border-t border-gray-800">
          <div className="text-sm text-gray-400 truncate">{userName}</div>
        </div>
      </div>
    </div>
  );
};
