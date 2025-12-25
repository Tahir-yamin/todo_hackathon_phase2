'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { MessageSquare, Brain, Sparkles } from 'lucide-react';

interface Step {
    title: string;
    subtitle: string;
    description: string;
    icon: React.ElementType;
    position: 'left' | 'right';
}

const steps: Step[] = [
    {
        title: 'The Brain Dump',
        subtitle: 'Input',
        description: 'Throw messy thoughts, voice notes, or Slack messages into the inbox.',
        icon: MessageSquare,
        position: 'left',
    },
    {
        title: 'Neural Analysis',
        subtitle: 'Process',
        description: 'Our AI Core scans context, urgency, and your habits instantly.',
        icon: Brain,
        position: 'right',
    },
    {
        title: 'Perfect Flow',
        subtitle: 'Output',
        description: 'Receive a perfectly ordered, conflict-free schedule for deep work.',
        icon: Sparkles,
        position: 'left',
    },
];

export function HowItWorksSection() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, margin: '-100px' });

    return (
        <section className="relative min-h-screen bg-gradient-to-b from-black via-slate-950 to-black py-24 overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
          w-[600px] h-[600px] bg-purple-500/5 rounded-full blur-[100px]" />
            </div>

            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-20"
                >
                    <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
                        <span className="block">How it</span>
                        <span className="block bg-gradient-to-r from-purple-400 via-pink-500 to-purple-600 
              bg-clip-text text-transparent">
                            actually works
                        </span>
                    </h2>
                    <p className="text-xl text-slate-400 max-w-2xl mx-auto">
                        Watch your chaos transform into clarity in three intelligent steps
                    </p>
                </motion.div>

                {/* Connected Intelligence Stream */}
                <div ref={ref} className="relative max-w-4xl mx-auto">
                    {/* Central Glowing Line with Pulse */}
                    <div className="absolute left-1/2 top-0 bottom-0 w-0.5 -translate-x-1/2">
                        {/* Base gradient line */}
                        <div className="absolute inset-0 bg-gradient-to-b from-purple-500 via-pink-500 to-purple-600 opacity-50" />

                        {/* Animated glow */}
                        <motion.div
                            className="absolute inset-0 bg-gradient-to-b from-transparent via-white to-transparent blur-sm"
                            animate={{
                                y: ['-100%', '200%'],
                            }}
                            transition={{
                                duration: 3,
                                repeat: Infinity,
                                ease: 'linear',
                            }}
                        />

                        {/* Flowing particles */}
                        {[0, 1, 2, 3, 4].map((i) => (
                            <motion.div
                                key={i}
                                className="absolute left-1/2 w-2 h-2 -translate-x-1/2 rounded-full bg-white shadow-[0_0_10px_rgba(255,255,255,0.8)]"
                                initial={{ y: -20, opacity: 0 }}
                                animate={{
                                    y: ['0%', '100%'],
                                    opacity: [0, 1, 1, 0],
                                }}
                                transition={{
                                    duration: 4,
                                    repeat: Infinity,
                                    delay: i * 0.8,
                                    ease: 'linear',
                                }}
                            />
                        ))}
                    </div>

                    {/* Steps */}
                    <div className="relative space-y-32">
                        {steps.map((step, index) => (
                            <StepCard key={index} step={step} index={index} isInView={isInView} />
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}

function StepCard({ step, index, isInView }: { step: Step; index: number; isInView: boolean }) {
    const Icon = step.icon;
    const isLeft = step.position === 'left';

    return (
        <motion.div
            initial={{
                opacity: 0,
                x: isLeft ? -100 : 100,
            }}
            animate={isInView ? {
                opacity: 1,
                x: 0,
            } : {}}
            transition={{
                duration: 0.8,
                delay: index * 0.3,
                type: 'spring',
                stiffness: 100,
            }}
            className={`relative flex ${isLeft ? 'justify-start' : 'justify-end'}`}
        >
            {/* Connection Node (Circle on the line) */}
            <motion.div
                initial={{ scale: 0 }}
                animate={isInView ? { scale: 1 } : {}}
                transition={{ delay: index * 0.3 + 0.4, type: 'spring', stiffness: 200 }}
                className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 
          w-6 h-6 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 
          shadow-[0_0_20px_rgba(168,85,247,0.6)] z-10"
            >
                <motion.div
                    className="absolute inset-0 rounded-full bg-white/30"
                    animate={{
                        scale: [1, 1.5, 1],
                        opacity: [0.5, 0, 0.5],
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        delay: index * 0.5,
                    }}
                />
            </motion.div>

            {/* Glass Card */}
            <motion.div
                whileHover={{ y: -5, scale: 1.02 }}
                className={`w-full max-w-md ${isLeft ? 'mr-auto pr-12' : 'ml-auto pl-12'}`}
            >
                <div className="relative group">
                    {/* Hover glow */}
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 to-pink-500/20 
            rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                    {/* Card content */}
                    <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 
            rounded-3xl p-8 shadow-[0_8px_32px_rgba(0,0,0,0.4)]
            group-hover:border-white/20 transition-all">

                        {/* Step number badge */}
                        <div className="absolute -top-3 left-6 px-4 py-1 bg-gradient-to-r from-purple-600 to-pink-600 
              rounded-full text-white text-sm font-bold shadow-lg">
                            Step {index + 1}
                        </div>

                        {/* Icon */}
                        <motion.div
                            whileHover={{ rotate: [0, -10, 10, -10, 0], scale: 1.1 }}
                            transition={{ duration: 0.5 }}
                            className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 
                flex items-center justify-center mb-6
                group-hover:shadow-[0_0_30px_rgba(168,85,247,0.3)] transition-shadow"
                        >
                            <Icon className="w-8 h-8 text-white" />
                        </motion.div>

                        {/* Content */}
                        <div className="space-y-2 mb-4">
                            <div className="text-purple-400 text-sm font-semibold uppercase tracking-wider">
                                {step.subtitle}
                            </div>
                            <h3 className="text-2xl font-bold text-white">
                                {step.title}
                            </h3>
                        </div>

                        <p className="text-slate-400 leading-relaxed">
                            {step.description}
                        </p>

                        {/* Animated connection line to center */}
                        <svg
                            className={`absolute top-1/2 ${isLeft ? 'right-0 translate-x-full' : 'left-0 -translate-x-full'} 
                w-12 h-0.5 -translate-y-1/2`}
                            style={{ overflow: 'visible' }}
                        >
                            <motion.line
                                x1={isLeft ? '0' : '48'}
                                y1="0"
                                x2={isLeft ? '48' : '0'}
                                y2="0"
                                stroke="url(#gradient)"
                                strokeWidth="2"
                                initial={{ pathLength: 0, opacity: 0 }}
                                animate={isInView ? { pathLength: 1, opacity: 0.5 } : {}}
                                transition={{ delay: index * 0.3 + 0.6, duration: 0.8 }}
                            />
                            <defs>
                                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stopColor="#a855f7" />
                                    <stop offset="100%" stopColor="#ec4899" />
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                </div>
            </motion.div>
        </motion.div>
    );
}
