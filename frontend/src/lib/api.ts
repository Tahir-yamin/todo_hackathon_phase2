const API_URL = 'http://localhost:8001';

// Helper function to get token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
};

// Helper function to add auth headers to requests
const getAuthHeaders = () => {
  const token = getAuthToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

export const api = {
  getTasks: async () => {
    const res = await fetch(`${API_URL}/api/tasks`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      if (res.status === 401) {
        // Redirect to login if unauthorized
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to fetch');
    }
    return res.json();
  },

  createTask: async (taskData: any) => {
    const res = await fetch(`${API_URL}/api/tasks`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to create');
    }
    return res.json();
  },

  updateTask: async (id: string, updates: any) => {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updates),
    });
    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to update');
    }
    return res.json();
  },

  deleteTask: async (id: string) => {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to delete');
    }
    return res.json();
  },

  // Authentication methods
  login: async (email: string, password: string) => {
    const res = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');
    return data;
  },

  register: async (username: string, email: string, password: string) => {
    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');
    return data;
  },

  logout: () => {
    localStorage.removeItem('token');
  },

  getCurrentUser: () => {
    const token = getAuthToken();
    if (!token) return null;

    try {
      // Decode JWT token to get user info (simplified - in real app you'd verify the token properly)
      const payload = token.split('.')[1];
      const decoded = JSON.parse(atob(payload));
      return decoded;
    } catch (error) {
      return null;
    }
  }
};
