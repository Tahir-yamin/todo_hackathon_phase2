import { authClient } from './auth-client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

// Get auth headers with real user ID from session
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
      // NUCLEAR DEV BYPASS: Don't redirect on 401
      // if (res.status === 401) {
      //   window.location.href = '/auth';
      //   throw new Error('Authentication required');
      // }
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
      // NUCLEAR DEV BYPASS: Don't redirect on 401
      // if (res.status === 401) {
      //   window.location.href = '/auth';
      //   throw new Error('Authentication required');
      // }
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
      // NUCLEAR DEV BYPASS: Don't redirect on 401
      // if (res.status === 401) {
      //   window.location.href = '/auth';
      //   throw new Error('Authentication required');
      // }
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
      // NUCLEAR DEV BYPASS: Don't redirect on 401
      // if (res.status === 401) {
      //   window.location.href = '/auth';
      //   throw new Error('Authentication required');
      // }
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to delete task');
    }

    // Return success - some DELETE endpoints return empty body
    try {
      return await res.json();
    } catch {
      return { success: true };
    }
  },
};
