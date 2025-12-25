'use client';

import React, { useState } from 'react';
import { ChevronLeft, Plus, Sparkles } from 'lucide-react';
import TaskForm from './TaskForm';

interface SidebarProps {
    onTaskCreated: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onTaskCreated }) => {
    const [isOpen, setIsOpen] = useState(true);

    return (
        <aside
            className={`${isOpen ? 'w-[320px]' : 'w-16'
                } bg-white/5 dark:bg-white/5 bg-slate-100/80 backdrop-blur-xl border-r dark:border-white/10 border-slate-300 relative transition-all duration-300 flex flex-col overflow-hidden z-50`}
        >
            {/* Toggle Button */}
            <div className="absolute top-4 right-4 z-20">
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="p-2 dark:bg-white/5 bg-white border dark:border-white/10 border-slate-300 rounded-xl dark:text-purple-400 text-purple-600 dark:hover:text-purple-300 hover:text-purple-700 dark:hover:border-white/20 hover:border-purple-300 transition-all"
                    title="Toggle Sidebar"
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
                <div className="flex flex-col h-full pt-16">
                    {/* Header */}
                    <div className="px-6 py-4 border-b dark:border-white/10 border-slate-300">
                        <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center shadow-[0_0_20px_rgba(168,85,247,0.3)] dark:border-white/10 border-purple-200 border">
                                <Sparkles className="w-5 h-5 dark:text-purple-400 text-purple-600" />
                            </div>
                            <div>
                                <h2 className="text-lg font-bold dark:text-white text-slate-900">Add New Task</h2>
                                <p className="text-xs dark:text-slate-400 text-slate-600">Create with AI or manually</p>
                            </div>
                        </div>
                    </div>

                    {/* Task Form */}
                    <div className="p-6 flex-1 overflow-y-auto custom-scrollbar">
                        <TaskForm onTaskCreated={onTaskCreated} inSidebar={true} />
                    </div>

                    {/* Footer tip */}
                    <div className="p-4 border-t dark:border-white/10 border-slate-300 dark:bg-white/5 bg-purple-50">
                        <div className="flex items-start gap-2 text-xs dark:text-slate-400 text-slate-600">
                            <Sparkles className="w-4 h-4 dark:text-purple-400 text-purple-600 flex-shrink-0 mt-0.5" />
                            <p>
                                <span className="dark:text-purple-400 text-purple-600 font-medium">Pro tip:</span> Use natural language to create tasks via the chat widget!
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Collapsed State Icon */}
            {!isOpen && (
                <div className="flex flex-col items-center justify-center h-full gap-4">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center shadow-[0_0_20px_rgba(168,85,247,0.3)] border border-white/10">
                        <Sparkles className="w-5 h-5 text-purple-400" />
                    </div>
                </div>
            )}
        </aside>
    );
};
