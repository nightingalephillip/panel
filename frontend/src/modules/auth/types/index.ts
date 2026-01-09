// User types
export interface User {
  id: string;
  email: string;
  displayName: string;
  role: UserRole;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export type UserRole = 'admin' | 'analyst' | 'viewer';

// Auth request types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  displayName: string;
}

// Auth response types
export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserApiResponse;
}

export interface UserApiResponse {
  id: string;
  email: string;
  display_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Auth state
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Transform API response to frontend User type
export function transformUser(apiUser: UserApiResponse): User {
  return {
    id: apiUser.id,
    email: apiUser.email,
    displayName: apiUser.display_name,
    role: apiUser.role,
    isActive: apiUser.is_active,
    createdAt: apiUser.created_at,
    updatedAt: apiUser.updated_at,
  };
}
