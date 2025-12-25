'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Calendar, Tag, CheckCircle2 } from 'lucide-react';

type DemoState = 'input' | 'processing' | 'result';

export function InteractiveDemo() {
    const [state, setState] = useState<DemoState>('input');
    const [input, setInput] = useState('');

    const handleMagic = async () => {
        if (!input.trim()) return;
        setState('processing');
        await new Promise(resolve => setTimeout(resolve, 2000));
        setState('result');
    };

    const handleReset = () => {
        setState('input');
        setInput('');
    };

    return (
        <section className="relative min-h-screen bg-gradient-to-b from-black to-slate-950 
      py-24 flex items-center justify-center overflow-hidden">
            {/* Background glow */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
          w-[800px] h-[800px] bg-purple-500/10 rounded-full blur-[120px]" />
            </div>

            <div className="relative z-10 w-full max-w-2xl mx-auto px-4">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-12"
                >
                    <h2 className="text-4xl sm:text-5xl font-bold text-white mb-4">
                        See the <span className="bg-gradient-to-r from-purple-400 to-pink-500 
              bg-clip-text text-transparent">magic</span> happen
                    </h2>
                    <p className="text-slate-400 text-lg">
                        Type a messy task and watch AI organize it instantly
                    </p>
                </motion.div>

                {/* Interactive Container */}
                <div className="relative bg-slate-900/50 backdrop-blur-xl border border-purple-500/20 
          rounded-3xl p-8 shadow-[0_0_50px_rgba(168,85,247,0.15)]">

                    <AnimatePresence mode="wait">
                        {/* INPUT STATE */}
                        {state === 'input' && (
                            <motion.div
                                key="input"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                className="space-y-4"
                            >
                                <div className="relative">
                                    <textarea
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        placeholder="e.g., Need to finish the Q3 report by Friday and email Sarah..."
                                        className="w-full h-32 bg-white/5 border border-white/10 rounded-2xl 
                      px-4 py-3 text-white placeholder:text-slate-500 outline-none 
                      focus:border-purple-500/50 transition-colors resize-none"
                                    />
                                </div>

                                <motion.button
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    onClick={handleMagic}
                                    disabled={!input.trim()}
                                    className="w-full px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 
                    rounded-full text-white font-semibold flex items-center justify-center gap-2
                    disabled:opacity-50 disabled:cursor-not-allowed
                    shadow-lg hover:shadow-purple-500/50 transition-all"
                                >
                                    <Sparkles className="w-5 h-5" />
                                    <span>Transform with AI</span>
                                </motion.button>
                            </motion.div>
                        )}

                        {/* PROCESSING STATE */}
                        {state === 'processing' && (
                            <motion.div
                                key="processing"
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 1.2 }}
                                className="flex flex-col items-center justify-center py-12"
                            >
                                {/* Neural Pulse */}
                                <div className="relative">
                                    <motion.div
                                        className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 
                      flex items-center justify-center"
                                        animate={{
                                            scale: [1, 1.2, 1],
                                            opacity: [1, 0.8, 1],
                                        }}
                                        transition={{
                                            duration: 1.5,
                                            repeat: Infinity,
                                            ease: 'easeInOut',
                                        }}
                                    >
                                        <Sparkles className="w-12 h-12 text-white" />
                                    </motion.div>

                                    {/* Rings */}
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
                                            }}
                                        />
                                    ))}
                                </div>

                                <motion.p
                                    className="mt-6 text-white/60"
                                    animate={{ opacity: [0.6, 1, 0.6] }}
                                    transition={{ duration: 1.5, repeat: Infinity }}
                                >
                                    AI is analyzing your task...
                                </motion.p>
                            </motion.div>
                        )}

                        {/* RESULT STATE */}
                        {state === 'result' && (
                            <motion.div
                                key="result"
                                initial={{ opacity: 0, rotateX: 90, y: 50 }}
                                animate={{ opacity: 1, rotateX: 0, y: 0 }}
                                transition={{ type: 'spring', stiffness: 200, damping: 20 }}
                                style={{ transformStyle: 'preserve-3d' }}
                            >
                                {/* Success Card */}
                                <div className="bg-white/10 backdrop-blur-sm border border-white/20 
                  rounded-2xl p-6 space-y-4">

                                    {/* Header */}
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-2">
                                            <div className="w-8 h-8 rounded-full bg-green-500/20 
                        flex items-center justify-center">
                                                <CheckCircle2 className="w-5 h-5 text-green-400" />
                                            </div>
                                            <span className="text-white font-semibold">Organized!</span>
                                        </div>
                                        <button
                                            onClick={handleReset}
                                            className="text-sm text-purple-400 hover:text-purple-300"
                                        >
                                            Try another
                                        </button>
                                    </div>

                                    {/* Task Details */}
                                    <div className="space-y-3">
                                        <div className="flex items-start gap-3">
                                            <CheckCircle2 className="w-5 h-5 text-slate-400 mt-0.5" />
                                            <div className="flex-1">
                                                <h4 className="text-white font-semibold">Finish Q3 Report</h4>
                                                <div className="flex flex-wrap gap-2 mt-2">
                                                    <div className="flex items-center gap-1.5 px-3 py-1 
                            bg-red-500/20 border border-red-500/30 rounded-full text-xs 
                            text-red-400">
                                                        <Tag className="w-3 h-3" />
                                                        High Priority
                                                    </div>
                                                    <div className="flex items-center gap-1.5 px-3 py-1 
                            bg-blue-500/20 border border-blue-500/30 rounded-full text-xs 
                            text-blue-400">
                                                        <Calendar className="w-3 h-3" />
                                                        Due: Friday
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-start gap-3 pl-8">
                                            <CheckCircle2 className="w-4 h-4 text-slate-500 mt-0.5" />
                                            <span className="text-slate-400 text-sm">Email Sarah</span>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </section>
    );
}
