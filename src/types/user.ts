// User and authentication types
export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  context: string;
  createdAt: Date;
}

export interface UserRole {
  title: string;
  description: string;
}

export interface Conversation {
  id: string;
  userId: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  messageCount: number;
}

export const PREDEFINED_ROLES: UserRole[] = [
  { title: 'Student', description: 'Learning and educational assistance' },
  { title: 'Professional', description: 'Work and career guidance' },
  { title: 'Developer', description: 'Programming and technical help' },
  { title: 'Researcher', description: 'Research and analysis support' },
  { title: 'Creative', description: 'Creative and artistic projects' },
  { title: 'General', description: 'General purpose assistance' },
];
