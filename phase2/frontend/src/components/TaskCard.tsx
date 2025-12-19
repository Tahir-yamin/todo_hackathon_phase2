'use client';

import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Task } from '@/types';
import { Calendar, Tag, Trash2, Edit } from 'lucide-react';

interface TaskCardProps {
    task: Task;
    onDelete: (taskId: string) => Promise<void>;
    onEdit: (task: Task) => void;
    onToggleComplete: () => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({
    task,
    onDelete,
    onEdit,
    onToggleComplete
}) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id: task.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1
    };

    const priorityColors = {
        low: {
            border: 'border-l-green-500',
            bg: 'bg-green-900/10',
            badge: 'bg-green-900/50 text-green-300 shadow-glow-low',
            glow: 'shadow-glow-low'
        },
        medium: {
            border: 'border-l-yellow-500',
            bg: 'bg-yellow-900/10',
            badge: 'bg-yellow-900/50 text-yellow-300 shadow-glow-medium',
            glow: 'shadow-glow-medium'
        },
        high: {
            border: 'border-l-orange-500',
            bg: 'bg-orange-900/10',
            badge: 'bg-orange-900/50 text-orange-300 shadow-glow-high',
            glow: 'shadow-glow-high'
        }
    };

    const colors = priorityColors[task.priority];

    const formatDate = (dateString: string | null) => {
        if (!dateString) return null;
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    };

    const isCompleted = task.status === 'completed';

    return (
        <div
            ref={setNodeRef}
            style={style}
            className={`node-card group ${colors.border} ${colors.bg} ${colors.glow} relative overflow-hidden`}
        >
            {/* Animated background grid */}
            <div className="absolute inset-0 opacity-10 pointer-events-none">
                <div className="absolute inset-0" style={{
                    backgroundImage: 'linear-gradient(0deg, rgba(0,240,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0,240,255,0.1) 1px, transparent 1px)',
                    backgroundSize: '10px 10px'
                }}></div>
            </div>

            <div className="flex items-start gap-2 relative z-10">
                {/* Drag Handle */}
                <div
                    {...attributes}
                    {...listeners}
                    className="cursor-move touch-none text-text-dark hover:text-primary transition-colors mt-1"
                >
                    <div className="flex flex-col gap-0.5">
                        <div className="w-1 h-1 bg-current rounded-full opacity-60"></div>
                        <div className="w-1 h-1 bg-current rounded-full opacity-60"></div>
                        <div className="w-1 h-1 bg-current rounded-full opacity-60"></div>
                    </div>
                </div>

                <div className="flex-1 min-w-0">
                    {/* Title */}
                    <h4 className={`font-medium text-slate-100 mb-2 font-mono text-sm ${isCompleted ? 'line-through opacity-60' : ''}`}>
                        {task.title}
                    </h4>

                    {/* Description */}
                    {task.description && (
                        <p className="text-xs text-slate-400 mb-3 line-clamp-2 font-mono">
                            {task.description}
                        </p>
                    )}

                    {/* Metadata */}
                    <div className="flex flex-wrap items-center gap-2 mb-3">
                        {/* Priority Badge */}
                        <span className={`px-2 py-0.5 rounded-sm text-xs font-medium font-mono ${colors.badge}`}>
                            {task.priority.toUpperCase()}
                        </span>

                        {/* Category */}
                        {task.category && (
                            <span className="px-2 py-0.5 rounded-sm text-xs bg-slate-700/50 text-slate-300 border border-slate-600 font-mono">
                                {task.category}
                            </span>
                        )}

                        {/* Due Date */}
                        {task.due_date && (
                            <span className="flex items-center gap-1 text-xs text-slate-400 font-mono">
                                <Calendar className="w-3 h-3" />
                                {formatDate(task.due_date)}
                            </span>
                        )}
                    </div>

                    {/* Tags */}
                    {task.tags && (
                        <div className="flex items-center gap-1 mb-3">
                            <Tag className="w-3 h-3 text-slate-500" />
                            <span className="text-xs text-slate-500 font-mono">{task.tags}</span>
                        </div>
                    )}

                    {/* Actions */}
                    <div className="flex items-center gap-2 pt-2 border-t border-slate-700/50 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                            onClick={(e) => {
                                e.stopPropagation();
                                onToggleComplete();
                            }}
                            className={`px-2 py-1 rounded-sm text-xs font-medium font-mono transition-all ${isCompleted
                                ? 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                                : 'bg-green-600 text-white hover:bg-green-500 shadow-glow-sm'
                                }`}
                        >
                            {isCompleted ? '↩ REVERT' : '✓ PROCESS'}
                        </button>

                        <button
                            onClick={(e) => {
                                e.stopPropagation();
                                onEdit(task);
                            }}
                            className="p-1 text-slate-400 hover:text-cyan-400 transition-colors"
                            title="Edit"
                        >
                            <Edit className="w-3.5 h-3.5" />
                        </button>

                        <button
                            onClick={(e) => {
                                e.stopPropagation();
                                if (confirm('Delete this data packet?')) {
                                    onDelete(task.id);
                                }
                            }}
                            className="p-1 text-slate-400 hover:text-red-400 transition-colors"
                            title="Delete"
                        >
                            <Trash2 className="w-3.5 h-3.5" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};
