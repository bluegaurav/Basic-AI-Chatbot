import { MessageSquare, Sparkles, Zap, Shield } from 'lucide-react';

export const EmptyState = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'Smart Responses',
      description: 'Get intelligent answers to your questions',
    },
    {
      icon: Zap,
      title: 'Fast & Efficient',
      description: 'Quick responses in real-time',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your conversations are safe',
    },
  ];

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-8">
        <div className="flex justify-center">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-xl">
            <MessageSquare className="w-10 h-10 text-white" />
          </div>
        </div>
        
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-gray-900">
            Start a Conversation
          </h2>
          <p className="text-gray-500">
            Send a message to begin chatting with the AI assistant
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-4 rounded-xl bg-white border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
            >
              <feature.icon className="w-6 h-6 text-purple-500 mx-auto mb-2" />
              <h3 className="text-sm font-semibold text-gray-900 mb-1">
                {feature.title}
              </h3>
              <p className="text-xs text-gray-500">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="text-xs text-gray-400">
          Tip: Press <kbd className="px-2 py-1 bg-gray-100 rounded border border-gray-300">Enter</kbd> to send, <kbd className="px-2 py-1 bg-gray-100 rounded border border-gray-300">Shift + Enter</kbd> for new line
        </div>
      </div>
    </div>
  );
};
