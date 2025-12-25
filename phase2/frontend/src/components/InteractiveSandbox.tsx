'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Brain, CheckCircle2, Clock, Zap } from 'lucide-react';

type DemoState = 'idle' | 'processing' | 'complete';

interface Task {
    time: string;
    title: string;
    tag: string;
    tagColor: string;
}

const PRESET_PROMPTS = [
    "I have a meeting at 10am and need to finish the Q3 report",
    "Schedule yoga at 7am, work on presentation, and call mom",
    "Plan my day: gym, client meeting, team standup, code review",
];

const generateMockPlan = (input: string): Task[] => {
    // Simple AI simulation - in production, this would call your API
    const tasks: Task[] = [
        { time: '10:00 AM', title: 'Client Meeting', tag: 'High Priority', tagColor: 'bg-red-500/20 text-red-400 border-red-500/30' },
        { time: '11:30 AM', title: 'Deep Work: Q3 Report', tag: 'Focus Mode', tagColor: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
        { time: '02:00 PM', title: 'Team Standup', tag: 'Recurring', tagColor: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
        { time: '03:30 PM', title: 'Email Responses', tag: 'Low Priority', tagColor: 'bg-green-500/20 text-green-400 border-green-500/30' },
    ];

    return tasks;
};

export function InteractiveSandbox() {
    const [state, setState] = useState<DemoState>('idle');
    const [input, setInput] = useState('');
    const [plan, setPlan] = useState<Task[]>([]);

    const handleGenerate = async () => {
        if (!input.trim()) return;

        setState('processing');

        // Simulate AI processing
        await new Promise(resolve => setTimeout(resolve, 2500));

        const generatedPlan = generateMockPlan(input);
        setPlan(generatedPlan);
        setState('complete');
    };

    const handleReset = () => {
        setState('idle');
        setInput('');
        setPlan([]);
    };

    const handlePreset = (preset: string) => {
        setInput(preset);
    };

    return (
        <div className="relative w-full max-w-4xl mx-auto px-4">
            <AnimatePresence mode="wait">
                {/* IDLE STATE - Input Container */}
                {state === 'idle' && (
                    <motion.div
                        key="idle"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="space-y-6"
                    >
                        {/* Preset Buttons */}
                        <div className="flex flex-wrap gap-2 justify-center mb-4">
                            {PRESET_PROMPTS.map((preset, i) => (
                                <motion.button
                                    key={i}
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => handlePreset(preset)}
                                    className="px-4 py-2 bg-white/5 backdrop-blur-sm border border-white/10 
                    rounded-full text-sm text-white/70 hover:text-white hover:bg-white/10 
                    transition-all"
                                >
                                    {preset.slice(0, 30)}...
                                </motion.button>
                            ))}
                        </div>

                        {/* Glass Input Container */}
                        <motion.div
                            className="relative"
                            whileHover={{ scale: 1.02 }}
                            transition={{ type: 'spring', stiffness: 300 }}
                        >
                            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 
                rounded-full blur-xl" />

                            <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 
                rounded-full p-2 shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
                                <div className="flex items-center gap-3">
                                    <input
                                        type="text"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
                                        placeholder="Ask AI to organize your day..."
                                        className="flex-1 bg-transparent px-6 py-4 text-white placeholder:text-white/40 
                      outline-none text-lg"
                                    />

                                    <motion.button
                                        whileHover={{ scale: 1.1 }}
                                        whileTap={{ scale: 0.9 }}
                                        onClick={handleGenerate}
                                        disabled={!input.trim()}
                                        className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 
                      rounded-full text-white font-semibold flex items-center gap-2
                      disabled:opacity-50 disabled:cursor-not-allowed
                      shadow-lg hover:shadow-purple-500/50 transition-shadow"
                                    >
                                        <Sparkles className="w-5 h-5" />
                                        <span>Generate</span>
                                    </motion.button>
                                </div>
                            </div>
                        </motion.div>

                        {/* Hint Text */}
                        <motion.p
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.3 }}
                            className="text-center text-white/50 text-sm"
                        >
                            Try it now • No signup required • Experience the AI magic ✨
                        </motion.p>
                    </motion.div>
                )}

                {/* PROCESSING STATE - AI Orb */}
                {state === 'processing' && (
                    <motion.div
                        key="processing"
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 1.2 }}
                        className="flex flex-col items-center justify-center py-20"
                    >
                        {/* Pulsing Orb */}
                        <div className="relative">
                            {/* Outer Rings */}
                            {[0, 1, 2].map((i) => (
                                <motion.div
                                    key={i}
                                    className="absolute inset-0 rounded-full border-2 border-purple-500/30"
                                    initial={{ scale: 1, opacity: 0.8 }}
                                    animate={{
                                        scale: [1, 2, 2.5],
                                        opacity: [0.8, 0.4, 0],
                                    }}
                                    transition={{
                                        duration: 2,
                                        repeat: Infinity,
                                        delay: i * 0.4,
                                        ease: 'easeOut',
                                    }}
                                    style={{ width: '120px', height: '120px' }}
                                />
                            ))}

                            {/* Core Orb */}
                            <motion.div
                                className="relative w-32 h-32 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 
                  flex items-center justify-center shadow-[0_0_60px_rgba(168,85,247,0.6)]"
                                animate={{
                                    rotate: 360,
                                    scale: [1, 1.1, 1],
                                }}
                                transition={{
                                    rotate: { duration: 3, repeat: Infinity, ease: 'linear' },
                                    scale: { duration: 1.5, repeat: Infinity, ease: 'easeInOut' },
                                }}
                            >
                                <Brain className="w-16 h-16 text-white" />
                            </motion.div>
                        </div>

                        {/* Processing Text */}
                        <motion.div
                            className="mt-8 text-center"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                        >
                            <h3 className="text-2xl font-bold text-white mb-2">
                                AI is thinking...
                            </h3>
                            <motion.p
                                className="text-white/60"
                                animate={{ opacity: [0.6, 1, 0.6] }}
                                transition={{ duration: 1.5, repeat: Infinity }}
                            >
                                Analyzing your schedule • Optimizing priorities • Creating your perfect day
                            </motion.p>
                        </motion.div>
                    </motion.div>
                )}

                {/* COMPLETE STATE - Result Card */}
                {state === 'complete' && (
                    <motion.div
                        key="complete"
                        initial={{ opacity: 0, scale: 0.8, rotateX: 90 }}
                        animate={{
                            opacity: 1,
                            scale: 1,
                            rotateX: 0,
                            y: [0, -10, 0],
                        }}
                        transition={{
                            type: 'spring',
                            stiffness: 200,
                            damping: 20,
                            y: {
                                duration: 3,
                                repeat: Infinity,
                                ease: 'easeInOut',
                            },
                        }}
                        className="perspective-1000"
                    >
                        {/* 3D Glass Card */}
                        <div className="relative transform-gpu"
                            style={{
                                transform: 'rotateX(5deg) rotateY(-5deg)',
                                transformStyle: 'preserve-3d',
                            }}
                        >
                            {/* Glow Effect */}
                            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/30 to-pink-500/30 
                rounded-3xl blur-2xl" />

                            {/* Main Card */}
                            <div className="relative bg-white/10 backdrop-blur-2xl border border-white/20 
                rounded-3xl p-8 shadow-[0_8px_32px_rgba(0,0,0,0.5)]">

                                {/* Header */}
                                <div className="flex items-center justify-between mb-6">
                                    <div className="flex items-center gap-3">
                                        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 
                      flex items-center justify-center">
                                            <CheckCircle2 className="w-6 h-6 text-white" />
                                        </div>
                                        <div>
                                            <h3 className="text-2xl font-bold text-white">Your Optimized Day</h3>
                                            <p className="text-white/60 text-sm">AI-generated schedule</p>
                                        </div>
                                    </div>

                                    <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={handleReset}
                                        className="px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 
                      rounded-full text-white text-sm transition-colors"
                                    >
                                        Try Again
                                    </motion.button>
                                </div>

                                {/* Task List */}
                                <div className="space-y-3">
                                    {plan.map((task, i) => (
                                        <motion.div
                                            key={i}
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: i * 0.1 }}
                                            className="group bg-white/5 hover:bg-white/10 backdrop-blur-sm border border-white/10 
                        rounded-2xl p-4 transition-all cursor-pointer"
                                        >
                                            <div className="flex items-start gap-4">
                                                {/* Time */}
                                                <div className="flex items-center gap-2 min-w-[100px]">
                                                    <Clock className="w-4 h-4 text-purple-400" />
                                                    <span className="text-white/80 font-medium">{task.time}</span>
                                                </div>

                                                {/* Content */}
                                                <div className="flex-1">
                                                    <h4 className="text-white font-semibold mb-1 group-hover:text-purple-300 transition-colors">
                                                        {task.title}
                                                    </h4>
                                                    <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full 
                            border text-xs font-medium ${task.tagColor}`}>
                                                        {task.tag === 'Focus Mode' && <Zap className="w-3 h-3" />}
                                                        <span>{task.tag}</span>
                                                    </div>
                                                </div>

                                                {/* Checkbox */}
                                                <motion.div
                                                    whileHover={{ scale: 1.2 }}
                                                    whileTap={{ scale: 0.9 }}
                                                    className="w-6 h-6 rounded-full border-2 border-white/20 
                            group-hover:border-purple-400 transition-colors cursor-pointer"
                                                />
                                            </div>
                                        </motion.div>
                                    ))}
                                </div>

                                {/* Footer Stats */}
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.5 }}
                                    className="mt-6 pt-6 border-t border-white/10 flex justify-around text-center"
                                >
                                    <div>
                                        <div className="text-2xl font-bold text-white">{plan.length}</div>
                                        <div className="text-white/60 text-sm">Tasks Organized</div>
                                    </div>
                                    <div>
                                        <div className="text-2xl font-bold text-purple-400">6.5h</div>
                                        <div className="text-white/60 text-sm">Productive Time</div>
                                    </div>
                                    <div>
                                        <div className="text-2xl font-bold text-pink-400">100%</div>
                                        <div className="text-white/60 text-sm">AI Optimized</div>
                                    </div>
                                </motion.div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
