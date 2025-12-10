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
              className={`p-4 rounded-lg border transition-all duration-300 hover:shadow-lg hover:scale-[1.01] ${
                task.status === 'completed'
                  ? 'bg-slate-900/70 border-slate-800 opacity-80'
                  : 'bg-slate-900 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center mb-2">
                    <h3 className={`text-base font-medium truncate ${
                      task.status === 'completed'
                        ? 'line-through text-slate-400'
                        : 'text-slate-200'
                    }`}>
                      {task.title}
                    </h3>
                    <span className={`ml-2 text-xs px-2 py-1 rounded-full ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                    {task.category && (
                      <span className={`ml-2 text-xs px-2 py-1 rounded-full ${getCategoryColor(task.category)}`}>
                        {task.category}
                      </span>
                    )}
                  </div>

                  {task.description && (
                    <p className="text-sm text-slate-400 mb-2 truncate">
                      {task.description}
                    </p>
                  )}

                  {task.tags && renderTags(task.tags)}

                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-2">
                    {task.due_date && (
                      <span className="inline-flex items-center">
                        <span className="mr-1">📅</span>
                        {formatDate(task.due_date)}
                      </span>
                    )}
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs ${
                      task.status === 'completed'
                        ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                        : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                    }`}>
                      {task.status === 'completed' ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                </div>

                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => toggleTaskStatus(task)}
                    disabled={loadingTasks[task.id]}
                    className={`p-2 rounded-md ${
                      task.status === 'completed'
                        ? 'text-green-400 hover:bg-green-500/10 border border-green-500/20'
                        : 'text-slate-400 hover:bg-slate-800 border border-slate-700'
                    } disabled:opacity-50 transition-colors duration-200`}
                    title={task.status === 'completed' ? 'Mark as pending' : 'Mark as complete'}
                  >
                    {loadingTasks[task.id] ? (
                      <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    ) : task.status === 'completed' ? (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </button>

                  <button
                    onClick={() => deleteTask(task.id)}
                    disabled={loadingTasks[task.id]}
                    className="p-2 text-slate-400 hover:bg-red-500/10 hover:text-red-400 rounded-md border border-slate-700 disabled:opacity-50 transition-colors duration-200"
                    title="Delete task"
                  >
                    {loadingTasks[task.id] ? (
                      <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    )}
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