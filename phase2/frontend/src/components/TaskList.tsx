'use client';

import React, { useState, useCallback } from 'react';
import { api } from '@/lib/api';
import { Task } from '@/types';
import EditTaskModal from './EditTaskModal';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdated }) => {
  const [loadingTasks, setLoadingTasks] = useState<{ [key: string]: boolean }>({});
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const toggleTaskStatus = useCallback(async (task: Task) => {
    if (loadingTasks[task.id]) return;

    const newStatus = task.status === 'todo' ? 'completed' : 'todo';
    setLoadingTasks(prev => ({ ...prev, [task.id]: true }));

    try {
      await api.updateTask(task.id, {
        status: newStatus,
        completed_at: newStatus === 'completed' ? new Date().toISOString() : null
      });
      onTaskUpdated();
    } catch (err) {
      console.error('Error updating task:', err);
    } finally {
      setLoadingTasks(prev => ({ ...prev, [task.id]: false }));
    }
  }, [loadingTasks, onTaskUpdated]);

  const deleteTask = useCallback(async (id: string) => {
    if (loadingTasks[id]) return;

    setLoadingTasks(prev => ({ ...prev, [id]: true }));

    try {
      await api.deleteTask(id);
      onTaskUpdated();
    } catch (err) {
      console.error('Error deleting task:', err);
    } finally {
      setLoadingTasks(prev => ({ ...prev, [id]: false }));
    }
  }, [loadingTasks, onTaskUpdated]);

  const handleEditSave = useCallback(async (taskId: string, updates: Partial<Task>) => {
    try {
      await api.updateTask(taskId, updates);
      onTaskUpdated();
    } catch (err) {
      console.error('Error updating task:', err);
      throw err;
    }
  }, [onTaskUpdated]);

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-500 text-white';
      case 'medium': return 'bg-orange-500 text-white';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-slate-500 text-white';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Work': return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      case 'Personal': return 'bg-purple-500/20 text-purple-300 border border-purple-500/30';
      case 'Learning': return 'bg-teal-500/20 text-teal-300 border border-teal-500/30';
      case 'Others': return 'bg-gray-500/20 text-gray-300 border border-gray-500/30';
      default: return 'bg-slate-500/20 text-slate-300 border border-slate-500/30';
    }
  };

  const renderTags = (tags: string) => {
    if (!tags) return null;
    const tagList = tags.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
    return (
      <div className="flex flex-wrap gap-1 mt-2">
        {tagList.map((tag, index) => (
          <span
            key={index}
            className="text-xs px-2 py-1 bg-gray-700 text-slate-200 rounded-full"
          >
            {tag}
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-slate-900 p-6 rounded-xl shadow-xl border border-slate-800 transition-all duration-300">
      <h2 className="text-xl font-semibold mb-4 text-slate-200">Your Tasks</h2>

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-slate-500 mb-2 text-4xl">📋</div>
          <p className="text-slate-400">You are all caught up!</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map(task => (
            <div
              key={task.id}
              className={`p-4 rounded-lg border transition-all duration-300 hover:shadow-lg hover:scale-[1.01] ${task.status === 'completed'
                ? 'bg-slate-900/70 border-slate-800 opacity-80'
                : 'bg-slate-900 border-slate-800 hover:border-slate-700'
                }`}
            >
              <div className="flex items-start justify-between gap-3">
                {/* Task Content */}
                <div className="flex-1 min-w-0">
                  {/* Title and Priority */}
                  <div className="flex items-center gap-2 flex-wrap mb-2">
                    <h3 className={`text-base font-medium text-slate-200 ${task.status === 'completed' ? 'line-through opacity-60' : ''
                      }`}>
                      {task.title}
                    </h3>
                    <span className={`px-2 py-0.5 text-xs font-medium rounded ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                    {task.category && (
                      <span className={`px-2 py-0.5 text-xs font-medium rounded ${getCategoryColor(task.category)}`}>
                        {task.category}
                      </span>
                    )}
                  </div>

                  {/* Description */}
                  {task.description && (
                    <p className="text-sm text-slate-400 mb-2 break-words">
                      {task.description}
                    </p>
                  )}

                  {/* Tags */}
                  {task.tags && renderTags(task.tags)}

                  {/* Due Date */}
                  {task.due_date && (
                    <div className="flex items-center gap-1 mt-2 text-xs text-slate-500">
                      <svg className="w-3 h-3" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                        <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                      <span>Due: {formatDate(task.due_date)}</span>
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2 flex-shrink-0">
                  <button
                    onClick={() => toggleTaskStatus(task)}
                    disabled={loadingTasks[task.id]}
                    className={`px-3 py-1 text-xs font-medium rounded transition-colors ${task.status === 'completed'
                      ? 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                      : 'bg-green-600 text-white hover:bg-green-500'
                      } disabled:opacity-50 disabled:cursor-not-allowed`}
                  >
                    {loadingTasks[task.id] ? '...' : task.status === 'completed' ? '↩ Undo' : '✓ Done'}
                  </button>

                  <button
                    onClick={() => setEditingTask(task)}
                    className="px-3 py-1 text-xs font-medium rounded bg-blue-600 text-white hover:bg-blue-500 transition-colors"
                  >
                    ✎ Edit
                  </button>

                  <button
                    onClick={() => deleteTask(task.id)}
                    disabled={loadingTasks[task.id]}
                    className="px-3 py-1 text-xs font-medium rounded bg-red-600 text-white hover:bg-red-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loadingTasks[task.id] ? '...' : '× Delete'}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Edit Modal */}
      {editingTask && (
        <EditTaskModal
          task={editingTask}
          isOpen={!!editingTask}
          onClose={() => setEditingTask(null)}
          onSave={handleEditSave}
        />
      )}
    </div>
  );
};

export default TaskList;