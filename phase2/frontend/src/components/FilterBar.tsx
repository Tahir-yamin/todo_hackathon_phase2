'use client';

import React, { useState, useEffect } from 'react';
import { Search, X, Filter } from 'lucide-react';

interface FilterBarProps {
    onFilterChange: (filters: TaskFilters) => void;
}

export interface TaskFilters {
    search: string;
    priority: string;
    status: string;
    category: string;
}

export const FilterBar: React.FC<FilterBarProps> = ({ onFilterChange }) => {
    const [search, setSearch] = useState('');
    const [priority, setPriority] = useState('all');
    const [status, setStatus] = useState('all');
    const [category, setCategory] = useState('');
    const [isExpanded, setIsExpanded] = useState(false);

    // Debounce search
    useEffect(() => {
        const timer = setTimeout(() => {
            onFilterChange({ search, priority, status, category });
        }, 300);

        return () => clearTimeout(timer);
    }, [search, priority, status, category]);

    const clearFilters = () => {
        setSearch('');
        setPriority('all');
        setStatus('all');
        setCategory('');
    };

    const hasActiveFilters = search || priority !== 'all' || status !== 'all' || category;

    return (
        <div className="cyber-panel mb-6 backdrop-blur-lg">
            {/* Main Search Bar */}
            <div className="p-4 flex items-center gap-3">
                {/* Search Input */}
                <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-dark" />
                    <input
                        type="text"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        placeholder="Search tasks..."
                        className="cyber-input w-full pl-10 pr-10 py-2"
                    />
                    {search && (
                        <button
                            onClick={() => setSearch('')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-text-dark hover:text-primary transition-colors"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    )}
                </div>

                {/* Filter Toggle Button */}
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className={`px-4 py-2 rounded-sm font-mono text-sm transition-all flex items-center gap-2 ${isExpanded || hasActiveFilters
                            ? 'bg-primary text-background-dark shadow-glow-sm'
                            : 'bg-slate-800 text-text-light hover:bg-slate-700'
                        }`}
                >
                    <Filter className="w-4 h-4" />
                    Filters
                    {hasActiveFilters && !isExpanded && (
                        <span className="bg-orange-500 w-2 h-2 rounded-full animate-glow-pulse"></span>
                    )}
                </button>

                {/* Clear Filters */}
                {hasActiveFilters && (
                    <button
                        onClick={clearFilters}
                        className="px-4 py-2 rounded-sm font-mono text-sm bg-red-900/50 text-red-400 hover:bg-red-900/70 transition-colors"
                    >
                        Clear
                    </button>
                )}
            </div>

            {/* Expanded Filters */}
            {isExpanded && (
                <div className="px-4 pb-4 grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-border-subtle pt-4 animate-fade-in">
                    {/* Priority Filter */}
                    <div>
                        <label className="block text-xs font-mono text-text-dark mb-2">PRIORITY</label>
                        <select
                            value={priority}
                            onChange={(e) => setPriority(e.target.value)}
                            className="cyber-input w-full py-2"
                        >
                            <option value="all">All Priorities</option>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>

                    {/* Status Filter */}
                    <div>
                        <label className="block text-xs font-mono text-text-dark mb-2">STATUS</label>
                        <select
                            value={status}
                            onChange={(e) => setStatus(e.target.value)}
                            className="cyber-input w-full py-2"
                        >
                            <option value="all">All Status</option>
                            <option value="todo">Todo</option>
                            <option value="in_progress">In Progress</option>
                            <option value="completed">Completed</option>
                        </select>
                    </div>

                    {/* Category Filter */}
                    <div>
                        <label className="block text-xs font-mono text-text-dark mb-2">CATEGORY</label>
                        <input
                            type="text"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            placeholder="Filter by category..."
                            className="cyber-input w-full py-2"
                        />
                    </div>
                </div>
            )}
        </div>
    );
};
