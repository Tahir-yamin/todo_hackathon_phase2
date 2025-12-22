'use client';

import React from 'react';
import {
    DndContext,
    DragEndEvent,
    DragOverlay,
    DragStartEvent,
    closestCorners,
    PointerSensor,
    useSensor,
    useSensors,
    MouseSensor,
    TouchSensor
} from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { Task } from '@/types';
import { KanbanColumn } from './KanbanColumn';
import { TaskCard } from './TaskCard';

interface KanbanBoardProps {
    tasks: Task[];
    onTaskUpdate: (taskId: string, updates: Partial<Task>) => Promise<void>;
    onTaskDelete: (taskId: string) => Promise<void>;
    onTaskEdit: (task: Task) => void;
}

export const KanbanBoard: React.FC<KanbanBoardProps> = ({
    tasks,
    onTaskUpdate,
    onTaskDelete,
    onTaskEdit
}) => {
    const [activeTask, setActiveTask] = React.useState<Task | null>(null);

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8,
            },
        }),
        useSensor(MouseSensor, {
            activationConstraint: {
                distance: 8,
            },
        }),
        useSensor(TouchSensor, {
            activationConstraint: {
                delay: 200,
                tolerance: 5,
            },
        })
    );

    // Group tasks by status
    const todoTasks = tasks.filter(t => t.status === 'pending');
    const inProgressTasks = tasks.filter(t => t.status === 'in_progress');
    const doneTasks = tasks.filter(t => t.status === 'completed');

    // Calculate analytics
    const totalTasks = tasks.length;
    const completedToday = doneTasks.filter(t => {
        if (!t.completed_at) return false;
        const completedDate = new Date(t.completed_at);
        const today = new Date();
        return completedDate.toDateString() === today.toDateString();
    }).length;
    const completionRate = totalTasks > 0 ? Math.round((doneTasks.length / totalTasks) * 100) : 0;
    const highPriorityCount = tasks.filter(t => t.priority === 'high').length;
    const overdueTasks = tasks.filter(t => {
        if (!t.due_date || t.status === 'completed') return false;
        return new Date(t.due_date) < new Date();
    }).length;

    const handleDragStart = (event: DragStartEvent) => {
        const task = tasks.find(t => t.id === event.active.id);
        setActiveTask(task || null);
    };

    const handleDragEnd = async (event: DragEndEvent) => {
        const { active, over } = event;
        setActiveTask(null);

        if (!over) return;

        const taskId = active.id as string;
        const newColumn = over.id as string;

        const task = tasks.find(t => t.id === taskId);
        if (!task) return;

        if (
            (newColumn === 'todo' && task.status === 'todo') ||
            (newColumn === 'in-progress' && task.status === 'in_progress') ||
            (newColumn === 'done' && task.status === 'completed')
        ) {
            return;
        }

        if (newColumn === 'done') {
            await onTaskUpdate(taskId, {
                status: 'completed',
                completed_at: new Date().toISOString()
            });
        } else if (newColumn === 'in-progress') {
            await onTaskUpdate(taskId, {
                status: 'in_progress',
                completed_at: null
            });
        } else if (newColumn === 'todo') {
            await onTaskUpdate(taskId, {
                status: 'todo',
                completed_at: null
            });
        }
    };

    return (
        <DndContext
            sensors={sensors}
            collisionDetection={closestCorners}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
        >
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {/* UNPROCESSED_DATA_ Column */}
                <KanbanColumn
                    id="todo"
                    title="UNPROCESSED_DATA_"
                    count={todoTasks.length}
                    color="slate"
                >
                    <SortableContext
                        items={todoTasks.map(t => t.id)}
                        strategy={verticalListSortingStrategy}
                    >
                        {todoTasks.map(task => (
                            <TaskCard
                                key={task.id}
                                task={task}
                                onDelete={onTaskDelete}
                                onEdit={onTaskEdit}
                                onToggleComplete={() => onTaskUpdate(task.id, {
                                    status: 'completed'
                                })}
                            />
                        ))}
                    </SortableContext>
                </KanbanColumn>

                {/* PROCESSING_NODES_ Column */}
                <KanbanColumn
                    id="in-progress"
                    title="PROCESSING_NODES_"
                    count={inProgressTasks.length}
                    color="blue"
                >
                    <SortableContext
                        items={inProgressTasks.map(t => t.id)}
                        strategy={verticalListSortingStrategy}
                    >
                        {inProgressTasks.map(task => (
                            <TaskCard
                                key={task.id}
                                task={task}
                                onDelete={onTaskDelete}
                                onEdit={onTaskEdit}
                                onToggleComplete={() => onTaskUpdate(task.id, {
                                    status: 'completed'
                                })}
                            />
                        ))}
                    </SortableContext>
                </KanbanColumn>

                {/* SYNTHESIZED_OUTPUT_ Column */}
                <KanbanColumn
                    id="done"
                    title="SYNTHESIZED_OUTPUT_"
                    count={doneTasks.length}
                    color="green"
                >
                    <SortableContext
                        items={doneTasks.map(t => t.id)}
                        strategy={verticalListSortingStrategy}
                    >
                        {doneTasks.map(task => (
                            <TaskCard
                                key={task.id}
                                task={task}
                                onDelete={onTaskDelete}
                                onEdit={onTaskEdit}
                                onToggleComplete={() => onTaskUpdate(task.id, {
                                    status: 'todo'
                                })}
                            />
                        ))}
                    </SortableContext>
                </KanbanColumn>

                {/* ANALYTICS_OVERVIEW_ Column - Now with real metrics! */}
                <div className="neural-column border-fuchsia-500/30 bg-fuchsia-900/10">
                    <div className="p-4 flex items-center justify-between border-b border-node-border bg-slate-900/80 sticky top-0 z-10 backdrop-blur-sm">
                        <div className="flex items-center gap-2">
                            <div className="data-point bg-fuchsia-500 animate-glow-pulse w-3 h-3 rounded-full"></div>
                            <h3 className="font-bold text-fuchsia-400 text-base font-mono tracking-wide">
                                ANALYTICS_OVERVIEW_
                            </h3>
                        </div>
                        <span className="bg-surface-dark/50 text-fuchsia-400 text-xs font-mono px-2 py-0.5 border border-border-subtle rounded-sm">
                            LIVE
                        </span>
                    </div>

                    {/* Real Analytics Content */}
                    <div className="p-4 space-y-4">
                        {/* Total Tasks */}
                        <div className="cyber-panel p-3 bg-slate-900/50">
                            <div className="flex items-center justify-between mb-1">
                                <span className="text-xs font-mono text-text-dark">TOTAL_TASKS</span>
                                <span className="text-2xl font-bold text-primary">{totalTasks}</span>
                            </div>
                            <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-primary animate-flow" style={{ width: '100%' }}></div>
                            </div>
                        </div>

                        {/* Completion Rate */}
                        <div className="cyber-panel p-3 bg-slate-900/50">
                            <div className="flex items-center justify-between mb-1">
                                <span className="text-xs font-mono text-text-dark">COMPLETION_RATE</span>
                                <span className="text-2xl font-bold text-green-400">{completionRate}%</span>
                            </div>
                            <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-green-500 transition-all duration-500"
                                    style={{ width: `${completionRate}%` }}
                                ></div>
                            </div>
                        </div>

                        {/* Completed Today */}
                        <div className="cyber-panel p-3 bg-slate-900/50">
                            <div className="flex items-center justify-between">
                                <span className="text-xs font-mono text-text-dark">COMPLETED_TODAY</span>
                                <span className="text-xl font-bold text-cyan-400">{completedToday}</span>
                            </div>
                        </div>

                        {/* High Priority */}
                        <div className="cyber-panel p-3 bg-slate-900/50">
                            <div className="flex items-center justify-between">
                                <span className="text-xs font-mono text-text-dark">HIGH_PRIORITY</span>
                                <span className="text-xl font-bold text-orange-400">{highPriorityCount}</span>
                            </div>
                        </div>

                        {/* Overdue */}
                        {overdueTasks > 0 && (
                            <div className="cyber-panel p-3 bg-red-900/20 border-red-500/30">
                                <div className="flex items-center justify-between">
                                    <span className="text-xs font-mono text-red-400">⚠️ OVERDUE_TASKS</span>
                                    <span className="text-xl font-bold text-red-400 animate-glow-pulse">{overdueTasks}</span>
                                </div>
                            </div>
                        )}

                        {/* Status Breakdown */}
                        <div className="cyber-panel p-3 bg-slate-900/50">
                            <div className="text-xs font-mono text-text-dark mb-2">STATUS_BREAKDOWN</div>
                            <div className="space-y-2">
                                <div className="flex items-center justify-between text-xs">
                                    <span className="text-slate-400">Todo</span>
                                    <span className="font-mono text-slate-300">{todoTasks.length}</span>
                                </div>
                                <div className="flex items-center justify-between text-xs">
                                    <span className="text-cyan-400">In Progress</span>
                                    <span className="font-mono text-cyan-300">{inProgressTasks.length}</span>
                                </div>
                                <div className="flex items-center justify-between text-xs">
                                    <span className="text-green-400">Done</span>
                                    <span className="font-mono text-green-300">{doneTasks.length}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Drag Overlay */}
            <DragOverlay>
                {activeTask ? (
                    <div className="opacity-50 rotate-2 scale-105">
                        <TaskCard
                            task={activeTask}
                            onDelete={() => { }}
                            onEdit={() => { }}
                            onToggleComplete={() => { }}
                        />
                    </div>
                ) : null}
            </DragOverlay>
        </DndContext>
    );
};
