const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Token storage key
const TOKEN_KEY = 'auth_token';

export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
};

export const setToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
};

export const removeToken = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
};

export const isAuthenticated = (): boolean => {
  return getToken() !== null;
};

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string;
}

export const register = async (
  email: string,
  password: string,
  fullName?: string
): Promise<User> => {
  const response = await fetch(`${API_URL}/api/v1/users/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, full_name: fullName }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }

  return response.json();
};

export const login = async (email: string, password: string): Promise<{ access_token: string }> => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  return response.json();
};

export const logout = async (): Promise<void> => {
  const token = getToken();
  if (!token) return;

  try {
    await fetch(`${API_URL}/api/v1/auth/logout`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch (error) {
    // Continue with client-side logout even if API call fails
    console.error('Logout API call failed:', error);
  }

  removeToken();
};

export const getCurrentUser = async (): Promise<User> => {
  const token = getToken();
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_URL}/api/v1/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error('Failed to get user');
  }

  return response.json();
};