'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Task } from '@/types';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  // Check authentication status on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);

    if (token) {
      fetchTasks();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await api.getTasks();
      setTasks(response.data.tasks || []);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError(err.response?.data?.detail || 'Failed to fetch tasks');

      // If unauthorized, redirect to login
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        localStorage.removeItem('token');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    router.push('/auth');
    router.refresh();
  };

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <p className="text-lg text-slate-200">Loading tasks...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 p-4 md:p-8">
      {/* Clean Top Navigation Bar */}
      <nav className="max-w-3xl mx-auto mb-6">
        <div className="flex justify-between items-center">
          <div className="text-center flex-1">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Manage Your Tasks
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-slate-800 text-slate-200 rounded-lg hover:bg-slate-700 transition-colors border border-slate-700 text-sm"
              >
                Sign Out
              </button>
            ) : (
              <>
                <a
                  href="/auth"
                  className="px-4 py-2 bg-slate-800 text-slate-200 rounded-lg hover:bg-slate-700 transition-colors border border-slate-700 text-sm"
                >
                  Login
                </a>
                <a
                  href="/auth"
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 transition-colors text-sm"
                >
                  Sign Up
                </a>
              </>
            )}
          </div>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto py-4">
        {/* Subtitle */}
        <div className="text-center mb-8">
          <p className="text-slate-400">Stay organized and boost your productivity</p>
        </div>

        {isAuthenticated ? (
          <>
            {error && (
              <div className="mb-6 p-4 bg-red-900/30 text-red-200 rounded-xl border border-red-800/50">
                {error}
              </div>
            )}

            <TaskForm onTaskCreated={fetchTasks} />

            <TaskList
              tasks={tasks}
              onTaskUpdated={fetchTasks}
            />
          </>
        ) : (
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-slate-200 mb-4">
              Welcome to Todoist
            </h2>
            <p className="text-slate-400 mb-8">
              Please log in to manage your tasks
            </p>
            <div className="space-x-4">
              <a
                href="/auth"
                className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 transition-colors"
              >
                Login
              </a>
              <a
                href="/auth"
                className="px-6 py-3 bg-slate-800 text-slate-200 rounded-lg hover:bg-slate-700 transition-colors border border-slate-700"
              >
                Sign Up
              </a>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}