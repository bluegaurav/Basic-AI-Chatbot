import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../lib/api';
import { User } from '../types/user';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  signup: (email: string, password: string, name: string) => Promise<boolean>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);

  const normalizeUser = (userData: any): User => ({
    id: String(userData.id),
    email: userData.email,
    name: userData.name,
    role: {
      title: userData.role?.title || userData.role_title || 'General',
      description:
        userData.role?.description ||
        userData.role_description ||
        'General purpose assistance',
    },
    context: userData.context || '',
    createdAt: new Date(userData.created_at || userData.createdAt || Date.now()),
  });

  // Load user from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem('chatbot_token');
    const savedUser = localStorage.getItem('chatbot_user');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(normalizeUser(userData));
      return;
    }

    if (token) {
      api
        .get('/users/me')
        .then((response) => {
          const currentUser = normalizeUser(response.data);
          setUser(currentUser);
          localStorage.setItem('chatbot_user', JSON.stringify(currentUser));
        })
        .catch(() => {
          localStorage.removeItem('chatbot_token');
          localStorage.removeItem('chatbot_user');
        });
    }
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const currentUser = normalizeUser(response.data.user);
      localStorage.setItem('chatbot_token', response.data.access_token);
      localStorage.setItem('chatbot_user', JSON.stringify(currentUser));
      setUser(currentUser);
      return true;
    } catch {
      return false;
    }
  };

  const signup = async (
    email: string,
    password: string,
    name: string
  ): Promise<boolean> => {
    try {
      const response = await api.post('/auth/signup', {
        email,
        password,
        name,
      });

      const currentUser = normalizeUser(response.data.user);
      localStorage.setItem('chatbot_token', response.data.access_token);
      localStorage.setItem('chatbot_user', JSON.stringify(currentUser));
      setUser(currentUser);
      return true;
    } catch {
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('chatbot_token');
    localStorage.removeItem('chatbot_user');
  };

  const updateUser = async (userData: Partial<User>) => {
    if (!user) return;

    try {
      const response = await api.put('/users/me', {
        name: userData.name ?? user.name,
        role_title: userData.role?.title ?? user.role.title,
        role_description: userData.role?.description ?? user.role.description,
        context: userData.context ?? user.context,
      });

      const updatedUser = normalizeUser(response.data);
      setUser(updatedUser);
      localStorage.setItem('chatbot_user', JSON.stringify(updatedUser));
    } catch {
      // Keep the existing local state if the backend update fails.
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        signup,
        logout,
        updateUser,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
