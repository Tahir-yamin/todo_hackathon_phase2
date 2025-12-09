'use client';

import React, { useState } from 'react';
import { api } from '@/lib/api';
import { Task } from '@/types';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdated }) => {
  const [loadingTasks, setLoadingTasks] = useState<{[key: string]: boolean}>({});

  const toggleTaskStatus = async (task: Task) => {
    const newStatus = task.status === 'pending' ? 'completed' : 'pending';
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
  };

  const deleteTask = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setLoadingTasks(prev => ({ ...prev, [id]: true }));

    try {
      await api.deleteTask(id);
      onTaskUpdated();
    } catch (err) {
      console.error('Error deleting task:', err);
    } finally {
      setLoadingTasks(prev => ({ ...prev, [id]: false }));
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100';
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Your Tasks</h2>

      {tasks.length === 0 ? (
        <p className="text-gray-500 dark:text-gray-400 text-center py-8">No tasks yet. Add your first task above!</p>
      ) : (
        <div className="space-y-4">
          {tasks.map(task => (
            <div
              key={task.id}
              className={`p-4 border rounded-md shadow-sm ${
                task.status === 'completed'
                  ? 'bg-gray-50 dark:bg-gray-700 opacity-75'
                  : 'bg-white dark:bg-gray-750'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center">
                    <h3 className={`text-lg font-medium ${
                      task.status === 'completed'
                        ? 'line-through text-gray-500 dark:text-gray-400'
                        : 'text-gray-800 dark:text-white'
                    }`}>
                      {task.title}
                    </h3>
                    <span className={`ml-2 text-xs px-2 py-1 rounded-full ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                  </div>

                  {task.description && (
                    <p className="mt-2 text-gray-600 dark:text-gray-300">
                      {task.description}
                    </p>
                  )}

                  <div className="mt-2 flex flex-wrap gap-2 text-sm text-gray-500 dark:text-gray-400">
                    {task.due_date && (
                      <span className="inline-flex items-center">
                        <span className="mr-1">📅</span>
                        Due: {formatDate(task.due_date)}
                      </span>
                    )}
                    <span className="inline-flex items-center">
                      <span className="mr-1">⏱️</span>
                      {task.status === 'completed' ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                </div>

                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => toggleTaskStatus(task)}
                    disabled={loadingTasks[task.id]}
                    className={`px-3 py-1 rounded-md text-sm font-medium ${
                      task.status === 'completed'
                        ? 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900 dark:text-green-100 dark:hover:bg-green-800'
                        : 'bg-blue-100 text-blue-800 hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-100 dark:hover:bg-blue-800'
                    } disabled:opacity-50`}
                  >
                    {loadingTasks[task.id] ? '...' : task.status === 'completed' ? 'Undo' : 'Complete'}
                  </button>

                  <button
                    onClick={() => deleteTask(task.id)}
                    disabled={loadingTasks[task.id]}
                    className="px-3 py-1 bg-red-100 text-red-800 hover:bg-red-200 rounded-md text-sm font-medium dark:bg-red-900 dark:text-red-100 dark:hover:bg-red-800 disabled:opacity-50"
                  >
                    {loadingTasks[task.id] ? '...' : 'Delete'}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;