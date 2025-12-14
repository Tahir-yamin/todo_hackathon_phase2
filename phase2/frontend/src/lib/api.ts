import { authClient } from './auth-client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

// Helper function to get auth headers with user ID
const getAuthHeaders = async () => {
  const session = await authClient.getSession();
  const userId = session?.data?.user?.id;

  return {
    'Content-Type': 'application/json',
    ...(userId && { 'X-User-ID': userId }),
  };
};

export const api = {
  getTasks: async () => {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/tasks/`, { headers }); // Added trailing slash

    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to fetch tasks');
    }
    return res.json();
  },

  createTask: async (taskData: any) => {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/tasks/`, { // Added trailing slash
      method: 'POST',
      headers,
      body: JSON.stringify(taskData),
    });

    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to create task');
    }
    return res.json();
  },

  updateTask: async (id: string, updates: any) => {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(updates),
    });

    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to update task');
    }
    return res.json();
  },

  deleteTask: async (id: string) => {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers,
    });

    if (!res.ok) {
      if (res.status === 401) {
        window.location.href = '/auth';
        throw new Error('Authentication required');
      }
      throw new Error('Failed to delete task');
    }
    return res.json();
  },
};
