'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession, signOut } from '@/lib/auth-client';
import { api } from '@/lib/api';
import { Task } from '@/types';
import { Sidebar } from '@/components/Sidebar';
import { ChatWidget } from '@/components/ChatWidget';
import TaskList from '@/components/TaskList';
import { KanbanBoard } from '@/components/KanbanBoard';
import EditTaskModal from '@/components/EditTaskModal';
import { FilterBar, TaskFilters } from '@/components/FilterBar';
import { LayoutList, LayoutGrid, Moon, Sun } from 'lucide-react';
import { ThemeProvider, useTheme } from '@/contexts/ThemeContext';

function HomeContent() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<'list' | 'kanban'>('kanban');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filters, setFilters] = useState<TaskFilters>({
    search: '',
    priority: 'all',
    status: 'all',
    category: ''
  });
  const router = useRouter();
  // Use real session from better-auth
  const { data: session, isPending } = useSession();
  const { theme, toggleTheme } = useTheme();

  // Redirect to auth if not authenticated
  useEffect(() => {
    if (!isPending && !session) {
      router.push('/auth');
    }
  }, [session, isPending, router]);

  // TEMPORARILY DISABLED: Fetch tasks immediately without waiting for session
  useEffect(() => {
    fetchTasks();
  }, []);

  // Apply local filtering
  useEffect(() => {
    let result = [...tasks];

    // Search filter
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchLower) ||
        (task.description && task.description.toLowerCase().includes(searchLower))
      );
    }

    // Priority filter
    if (filters.priority !== 'all') {
      result = result.filter(task => task.priority === filters.priority);
    }

    // Status filter
    if (filters.status !== 'all') {
      result = result.filter(task => task.status === filters.status);
    }

    // Category filter
    if (filters.category) {
      const categoryLower = filters.category.toLowerCase();
      result = result.filter(task =>
        task.category && task.category.toLowerCase().includes(categoryLower)
      );
    }

    setFilteredTasks(result);
  }, [tasks, filters]);

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

  const handleTaskUpdate = async (taskId: string, updates: Partial<Task>) => {
    try {
      await api.updateTask(taskId, updates);
      await fetchTasks();
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    try {
      await api.deleteTask(taskId);
      await fetchTasks();
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError(err.message || 'Failed to delete task');
    }
  };

  const handleLogout = async () => {
    await signOut();
    window.location.href = '/auth'; // Force hard redirect to auth page
  };

  const handleFilterChange = (newFilters: TaskFilters) => {
    setFilters(newFilters);
  };

  if (isPending || loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-background-dark">
        <p className="text-lg text-text-light font-mono">Loading...</p>
      </main>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="flex flex-col md:grid md:grid-cols-[auto_1fr] h-screen bg-background-dark">
      {/* Left Sidebar - Hidden on mobile by default */}
      <div className="hidden md:block">
        <Sidebar onTaskCreated={fetchTasks} />
      </div>

      {/* Main Content Area */}
      <main className="flex flex-col h-full relative">
        {/* Top Navigation - Always visible */}
        <nav className="cyber-panel px-6 h-16 flex justify-between items-center backdrop-blur-lg border-b border-accent/20 flex-shrink-0">
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-sm bg-primary flex items-center justify-center text-background-dark font-bold text-lg shadow-glow-sm">
              T
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white font-mono">TODO</h1>
              <p className="text-xs text-text-dark font-mono">Access Granted: {session.user.name || session.user.email}</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* View Toggle */}
            <div className="flex border border-border-subtle rounded-sm overflow-hidden">
              <button
                onClick={() => setView('list')}
                className={`px-3 py-1.5 text-sm font-medium font-mono transition-colors flex items-center gap-1 ${view === 'list'
                  ? 'bg-primary text-background-dark shadow-glow-sm'
                  : 'text-text-dark hover:text-primary'
                  }`}
              >
                <LayoutList className="w-4 h-4" />
                Task List
              </button>
              <button
                onClick={() => setView('kanban')}
                className={`px-3 py-1.5 text-sm font-medium font-mono transition-colors flex items-center gap-1 ${view === 'kanban'
                  ? 'bg-primary text-background-dark shadow-glow-sm'
                  : 'text-text-dark hover:text-primary'
                  }`}
              >
                <LayoutGrid className="w-4 h-4" />
                Kanban
              </button>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 text-text-dark hover:text-primary transition-colors"
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            <button
              onClick={handleLogout}
              className="text-sm font-medium font-mono text-text-dark hover:text-red-500 transition-colors"
            >
              Logout
            </button>
          </div>
        </nav>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-300 font-mono text-sm">
            {error}
          </div>
        )}

        {/* Filter Bar */}
        <FilterBar onFilterChange={handleFilterChange} />

        {/* View Content */}
        <div className="flex-1">
          {view === 'list' ? (
            <TaskList tasks={filteredTasks} onTaskUpdated={fetchTasks} />
          ) : (
            <KanbanBoard
              tasks={filteredTasks}
              onTaskUpdate={handleTaskUpdate}
              onTaskDelete={handleTaskDelete}
              onTaskEdit={(task) => setEditingTask(task)}
            />
          )}
        </div>

        {/* Edit Task Modal */}
        {editingTask && (
          <EditTaskModal
            task={editingTask}
            isOpen={!!editingTask}
            onClose={() => setEditingTask(null)}
            onSave={handleTaskUpdate}
          />
        )}
      </main>

      {/* Floating Chat Widget */}
      <ChatWidget />
    </div>
  );
}

export default function Home() {
  return (
    <ThemeProvider>
      <HomeContent />
    </ThemeProvider>
  );
}