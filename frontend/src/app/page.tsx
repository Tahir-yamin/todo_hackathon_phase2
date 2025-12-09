'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Task } from '@/types';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await api.getTasks();
      setTasks(response.data.tasks || []);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError(err.response?.data?.detail || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <p className="text-lg">Loading tasks...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800 dark:text-white">Todo App</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        <TaskForm onTaskCreated={fetchTasks} />

        <TaskList
          tasks={tasks}
          onTaskUpdated={fetchTasks}
        />
      </div>
    </main>
  );
}