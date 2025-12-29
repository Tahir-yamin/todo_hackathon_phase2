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

function DashboardContent() {
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
    const { data: session, isPending } = useSession();
    const { theme, toggleTheme } = useTheme();

    // Redirect to auth if not authenticated
    useEffect(() => {
        if (!isPending && !session) {
            router.push('/auth');
        }
    }, [session, isPending, router]);

    // Fetch tasks on mount and listen for global task updates
    useEffect(() => {
        // 1. Initial fetch
        fetchTasks();

        // 2. Define the event listener for cross-component updates
        const handleTaskUpdate = () => {
            console.log("🔄 Event received: Refreshing tasks from global event...");
            fetchTasks();
        };

        // 3. Subscribe to the "task-update" event from ChatWidget
        window.addEventListener('task-update', handleTaskUpdate);

        // 4. Cleanup listener when component unmounts
        return () => {
            window.removeEventListener('task-update', handleTaskUpdate);
        };
    }, []);

    // Apply local filtering
    useEffect(() => {
        let result = [...tasks];

        if (filters.search) {
            const searchLower = filters.search.toLowerCase();
            result = result.filter(task =>
                task.title.toLowerCase().includes(searchLower) ||
                (task.description && task.description.toLowerCase().includes(searchLower))
            );
        }

        if (filters.priority !== 'all') {
            result = result.filter(task => task.priority === filters.priority);
        }

        if (filters.status !== 'all') {
            result = result.filter(task => task.status === filters.status);
        }

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
        window.location.href = '/landing';
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
        <div className="flex flex-col md:grid md:grid-cols-[auto_1fr] h-screen bg-slate-950 relative overflow-hidden">
            {/* Animated Background Blobs - matching landing page */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-purple-500/10 rounded-full blur-[120px] animate-blob" />
                <div className="absolute top-[40%] right-[-5%] w-[500px] h-[500px] bg-pink-500/10 rounded-full blur-[120px] animate-blob animation-delay-2000" />
                <div className="absolute bottom-[-10%] left-[30%] w-[550px] h-[550px] bg-blue-500/10 rounded-full blur-[120px] animate-blob animation-delay-4000" />
            </div>

            <div className="hidden md:block relative z-10">
                <Sidebar onTaskCreated={fetchTasks} />
            </div>

            <main className="flex flex-col h-full overflow-hidden relative z-10">
                <nav className="px-6 h-16 flex justify-between items-center bg-white/5 backdrop-blur-xl border-b border-white/10 flex-shrink-0">
                    <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center shadow-[0_0_20px_rgba(168,85,247,0.3)] border border-white/10">
                            <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">T</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold tracking-tight text-white">AI Todo Dashboard</h1>
                            <p className="text-xs text-slate-400">{session.user.name || session.user.email}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <div className="flex bg-white/5 border border-white/10 rounded-xl overflow-hidden">
                            <button
                                onClick={() => setView('list')}
                                className={`px-4 py-2 text-sm font-medium transition-all duration-200 flex items-center gap-2 ${view === 'list'
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-[0_0_20px_rgba(168,85,247,0.4)]'
                                    : 'text-slate-400 hover:text-white'
                                    }`}
                            >
                                <LayoutList className="w-4 h-4" />
                                List
                            </button>
                            <button
                                onClick={() => setView('kanban')}
                                className={`px-4 py-2 text-sm font-medium transition-all duration-200 flex items-center gap-2 ${view === 'kanban'
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-[0_0_20px_rgba(168,85,247,0.4)]'
                                    : 'text-slate-400 hover:text-white'
                                    }`}
                            >
                                <LayoutGrid className="w-4 h-4" />
                                Kanban
                            </button>
                        </div>

                        <button
                            onClick={toggleTheme}
                            className="p-2 text-slate-400 hover:text-white transition-colors bg-white/5 border border-white/10 rounded-xl hover:border-white/20"
                            title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
                        >
                            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                        </button>

                        <button
                            onClick={handleLogout}
                            className="px-4 py-2 text-sm font-medium bg-white/5 border border-white/10 rounded-xl text-slate-400 hover:text-red-400 hover:border-red-400/50 transition-all duration-200"
                        >
                            Logout
                        </button>
                    </div>
                </nav>

                {error && (
                    <div className="mb-4 p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-300 font-mono text-sm">
                        {error}
                    </div>
                )}

                <FilterBar onFilterChange={handleFilterChange} />

                <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
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

                {editingTask && (
                    <EditTaskModal
                        task={editingTask}
                        isOpen={!!editingTask}
                        onClose={() => setEditingTask(null)}
                        onSave={handleTaskUpdate}
                    />
                )}
            </main>

            <ChatWidget />
        </div>
    );
}

export default function Dashboard() {
    return (
        <ThemeProvider>
            <DashboardContent />
        </ThemeProvider>
    );
}
