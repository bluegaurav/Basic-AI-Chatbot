// Configuration file for easy customization
export const chatConfig = {
  // App Information
  appName: 'AI Assistant',
  appTagline: 'Always here to help',
  
  // UI Settings
  maxMessageWidth: '75%', // For mobile
  maxMessageWidthDesktop: '70%', // For desktop
  
  // Behavior
  autoScroll: true,
  showTimestamps: true,
  enableKeyboardShortcuts: true,
  
  // Input Settings
  inputPlaceholder: 'Type your message...',
  maxInputHeight: '120px',
  minInputHeight: '48px',
  
  // Response Settings
  simulateTypingDelay: true,
  minTypingDelay: 1000, // milliseconds
  maxTypingDelay: 2000, // milliseconds
  
  // Features
  features: [
    {
      title: 'Smart Responses',
      description: 'Get intelligent answers to your questions',
    },
    {
      title: 'Fast & Efficient',
      description: 'Quick responses in real-time',
    },
    {
      title: 'Secure & Private',
      description: 'Your conversations are safe',
    },
  ],
  
  // Welcome Messages (optional)
  welcomeMessage: null, // Set to a string to display an initial message
  
  // API Configuration (to be filled when integrating)
  api: {
    endpoint: '', // Your API endpoint
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Add your headers here
    },
  },
};

export type ChatConfig = typeof chatConfig;
