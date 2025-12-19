'use client';

import React from 'react';
import { useDroppable } from '@dnd-kit/core';

interface KanbanColumnProps {
    id: string;
    title: string;
    count: number;
    color: 'slate' | 'blue' | 'green';
    children: React.ReactNode;
}

export const KanbanColumn: React.FC<KanbanColumnProps> = ({
    id,
    title,
    count,
    color,
    children
}) => {
    const { setNodeRef, isOver } = useDroppable({ id });

    const colorClasses = {
        slate: 'border-slate-500/30 bg-slate-900/20',
        blue: 'border-cyan-500/30 bg-cyan-900/10',
        green: 'border-green-500/30 bg-green-900/10'
    };

    const glowClasses = {
        slate: 'data-point bg-slate-500/50',
        blue: 'data-point bg-cyan-500 animate-glow-pulse',
        green: 'data-point bg-green-500 animate-glow-pulse'
    };

    const textClasses = {
        slate: 'text-slate-400',
        blue: 'text-cyan-400 glow-text',
        green: 'text-green-400 glow-text'
    };

    return (
        <div
            ref={setNodeRef}
            className={`neural-column ${colorClasses[color]} ${isOver ? 'shadow-glow-md scale-[1.01]' : ''
                } transition-all duration-300`}
        >
            {/* Neural Column Header */}
            <div className="p-4 flex items-center justify-between border-b border-node-border bg-slate-900/80 sticky top-0 z-10 backdrop-blur-sm">
                <div className="flex items-center gap-2">
                    <div className={`${glowClasses[color]} w-3 h-3 rounded-full`}></div>
                    <h3 className={`font-bold ${textClasses[color]} text-base font-mono tracking-wide`}>
                        {title}
                    </h3>
                </div>
                <span className="bg-surface-dark/50 text-text-dark text-xs font-mono px-2 py-0.5 border border-border-subtle rounded-sm">
                    {count}
                </span>
            </div>

            {/* Column Content */}
            <div className="p-4 space-y-3 flex-1 overflow-y-auto custom-scrollbar min-h-[400px]">
                {React.Children.count(children) > 0 ? (
                    children
                ) : (
                    <div className="flex flex-col items-center justify-center p-8 text-center text-text-dark/70 h-full">
                        <div className="w-12 h-12 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center text-primary/70 mb-3 animate-node-sparkle">
                            <span className="text-2xl">⚡</span>
                        </div>
                        <p className="text-sm font-mono">NO DATA STREAMED</p>
                        <p className="text-xs text-text-dark/50 mt-1">Drag tasks to this column</p>
                    </div>
                )}
            </div>
        </div>
    );
};
