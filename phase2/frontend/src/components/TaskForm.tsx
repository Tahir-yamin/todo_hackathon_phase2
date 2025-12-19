'use client';

import React, { useState } from 'react';
import { api } from '@/lib/api';
import { TaskFormData } from '@/types';
import { SmartTaskInput } from './SmartTaskInput';

interface TaskFormProps {
  onTaskCreated: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ onTaskCreated, inSidebar = false }) => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    description: '',
    priority: 'medium',
    due_date: '',
    category: 'Personal',
    tags: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAIParse = (parsedData: any) => {
    // Convert ISO datetime to date input format (YYYY-MM-DD)
    let dueDateValue = '';
    if (parsedData.due_date) {
      try {
        const date = new Date(parsedData.due_date);
        dueDateValue = date.toISOString().split('T')[0];
      } catch (e) {
        dueDateValue = '';
      }
    }

    setFormData({
      title: parsedData.title || '',
      description: '',
      priority: parsedData.priority || 'medium',
      due_date: dueDateValue,
      category: parsedData.category || 'Personal',
      tags: parsedData.tags || '',
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        due_date: formData.due_date ? new Date(formData.due_date).toISOString() : null,
      };
      await api.createTask(payload);
      setFormData({
        title: '',
        description: '',
        priority: 'medium',
        due_date: '',
        category: 'Personal',
        tags: '',
      });
      onTaskCreated();
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto mb-8">
      <form onSubmit={handleSubmit} className="bg-slate-900 rounded-lg p-6 shadow-lg border border-slate-800">
        <h2 className="text-xl font-semibold text-slate-100 mb-4">Add New Task</h2>

        {/* AI-Powered Smart Input */}
        <SmartTaskInput onParse={handleAIParse} />

        {error && (
          <div className="mb-4 p-3 bg-red-900/20 border border-red-800 rounded text-red-300 text-sm">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label htmlFor="title" className="block text-sm font-medium text-slate-300 mb-1">
              Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter task title"
            />
          </div>

          <div className="md:col-span-2">
            <label htmlFor="description" className="block text-sm font-medium text-slate-300 mb-1">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter task description"
            />
          </div>

          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-slate-300 mb-1">
              Priority
            </label>
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div>
            <label htmlFor="due_date" className="block text-sm font-medium text-slate-300 mb-1">
              Due Date
            </label>
            <input
              type="date"
              id="due_date"
              name="due_date"
              value={formData.due_date}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="category" className="block text-sm font-medium text-slate-300 mb-1">
              Category
            </label>
            <input
              type="text"
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="e.g., Work, Personal"
            />
          </div>

          <div>
            <label htmlFor="tags" className="block text-sm font-medium text-slate-300 mb-1">
              Tags
            </label>
            <input
              type="text"
              id="tags"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Comma-separated tags"
            />
          </div>
        </div>

        <div className="mt-4">
          <button
            type="submit"
            disabled={loading}
            className={`w-full md:w-auto px-6 py-2 rounded-lg font-medium transition-colors ${loading
              ? 'bg-indigo-800 text-slate-400 cursor-not-allowed'
              : 'bg-indigo-600 text-white hover:bg-indigo-500'
              }`}
          >
            {loading ? 'Creating...' : 'Add Task'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;