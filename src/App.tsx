import { AuthProvider, useAuth } from './context/AuthContext';
import { Login } from './components/Login';
import { ChatApp } from './components/ChatApp';

function AppContent() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Login />;
  }

  return <ChatApp />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
