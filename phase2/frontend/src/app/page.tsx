'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession, signOut } from '@/lib/auth-client';
import { api } from '@/lib/api';
import { Task } from '@/types';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Use Better Auth session
  const { data: session, isPending } = useSession();

  // Redirect to auth if not logged in
  useEffect(() => {
    if (!isPending && !session) {
      router.push('/auth');
    }
  }, [session, isPending, router]);

  // Fetch tasks when session is available
  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await api.getTasks();
      setTasks(response.data.tasks || []);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await signOut();
    router.push('/auth');
    router.refresh();
  };

  if (isPending || loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <p className="text-lg text-slate-200">Loading...</p>
      </main>
    );
  }

  if (!session) {
    return null; // Will redirect to /auth
  }

  return (
    <main className="min-h-screen bg-slate-950 p-4 md:p-8">
      {/* Navigation Bar */}
      <div className="max-w-7xl mx-auto mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-100">Todoist</h1>
          <p className="text-slate-400 mt-1">
            Welcome, {session.user.name || session.user.email}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-slate-800 text-slate-200 rounded-lg hover:bg-slate-700 transition-colors border border-slate-700"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      {error && (
        <div className="max-w-7xl mx-auto mb-4 p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-300">
          {error}
        </div>
      )}

      <TaskForm onTaskCreated={fetchTasks} />
      <TaskList tasks={tasks} onTaskUpdated={fetchTasks} />
    </main>
  );
}