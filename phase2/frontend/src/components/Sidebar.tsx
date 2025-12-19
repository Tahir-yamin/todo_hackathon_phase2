'use client';

import React, { useState } from 'react';
import { ChevronLeft, Plus } from 'lucide-react';
import TaskForm from './TaskForm';

interface SidebarProps {
    onTaskCreated: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onTaskCreated }) => {
    const [isOpen, setIsOpen] = useState(true);

    return (
        <aside
            className={`${isOpen ? 'w-[320px]' : 'w-16'
                } bg-background-dark/80 backdrop-blur-lg border-r border-border-grid relative transition-all duration-300 flex flex-col pt-16 overflow-hidden z-50`}
        >
            {/* Toggle Button */}
            <div className="absolute top-0 right-0 h-16 w-16 flex items-center justify-center z-20">
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="p-2 text-primary hover:text-primary-dark transition-colors"
                    title="Toggle AI Synthesis Engine"
                >
                    {isOpen ? (
                        <ChevronLeft className="w-5 h-5" />
                    ) : (
                        <Plus className="w-5 h-5" />
                    )}
                </button>
            </div>

            {/* Sidebar Content */}
            {isOpen && (
                <div className="flex flex-col h-full">
                    {/* Header */}
                    <div className="p-4 border-b border-border-subtle flex justify-between items-center bg-surface-dark/70 sticky top-0 z-10">
                        <h2 className="text-base font-bold text-primary flex items-center gap-2 font-mono">
                            <span className="text-lg">⚡</span> AI Synthesis Engine
                        </h2>
                        <span className="text-xs font-mono text-text-dark bg-surface-dark px-2 py-1 border border-border-subtle rounded-sm">
                            CMD+N
                        </span>
                    </div>

                    {/* Content - Just Visualization and Form */}
                    <div className="p-4 space-y-4 flex-1 overflow-y-auto custom-scrollbar">
                        {/* Synthesis Visualization */}
                        <div className="relative h-36 bg-background-dark border border-node-border overflow-hidden rounded-sm">
                            {/* Grid Background */}
                            <div
                                className="absolute inset-0 opacity-10 animate-flow"
                                style={{
                                    backgroundImage:
                                        'linear-gradient(0deg, rgba(0,240,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0,240,255,0.1) 1px, transparent 1px)',
                                    backgroundSize: '20px 20px',
                                }}
                            ></div>

                            {/* Central Content */}
                            <div className="absolute inset-0 flex flex-col items-center justify-center z-10">
                                <div className="w-16 h-16 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center text-primary/50 mb-2 animate-node-sparkle">
                                    <span className="text-2xl">📊</span>
                                </div>
                                <p className="text-xs font-mono text-primary/80">SYNTHESIS_VISUALIZATION</p>
                                <p className="text-[10px] text-text-dark/50 mt-1">Algorithmic Integration</p>
                            </div>

                            {/* Floating Nodes */}
                            <div className="absolute top-3 left-3 w-6 h-6 rounded-full bg-primary/30 blur-sm animate-node-sparkle"></div>
                            <div
                                className="absolute bottom-3 right-3 w-5 h-5 rounded-full bg-red-500/30 blur-sm animate-node-sparkle"
                                style={{ animationDelay: '1s' }}
                            ></div>
                            <div
                                className="absolute top-1/3 left-1/4 w-4 h-4 rounded-full bg-green-500/30 blur-sm animate-node-sparkle"
                                style={{ animationDelay: '2s' }}
                            ></div>
                        </div>

                        {/* Task Form - Full width in sidebar */}
                        <div className="space-y-3">
                            <TaskForm onTaskCreated={onTaskCreated} inSidebar={true} />
                        </div>
                    </div>
                </div>
            )}

            {/* Collapsed State Icon */}
            {!isOpen && (
                <div className="flex flex-col items-center justify-center h-full gap-4">
                    <span className="text-primary text-2xl">⚡</span>
                </div>
            )}
        </aside>
    );
};
