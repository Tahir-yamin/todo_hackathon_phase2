'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { Sparkles, Zap, Brain, LucideIcon } from 'lucide-react';

interface Feature {
    icon: LucideIcon;
    title: string;
    description: string;
    gradient: string;
}

const features: Feature[] = [
    {
        icon: Sparkles,
        title: 'Smart Sorting',
        description: 'AI automatically tags and prioritizes tasks based on urgency.',
        gradient: 'from-purple-500/20 to-pink-500/20',
    },
    {
        icon: Zap,
        title: 'Context Awareness',
        description: 'The interface adapts to your focus mode, hiding distractions.',
        gradient: 'from-blue-500/20 to-cyan-500/20',
    },
    {
        icon: Brain,
        title: 'Neural Sync',
        description: 'Seamlessly connects notes and tasks into one central brain.',
        gradient: 'from-purple-500/20 to-blue-500/20',
    },
];

// Animation variants for staggered entrance
const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.2,
            delayChildren: 0.1,
        },
    },
};

const cardVariants = {
    hidden: {
        opacity: 0,
        y: 50,
        scale: 0.95,
    },
    visible: {
        opacity: 1,
        y: 0,
        scale: 1,
        transition: {
            type: 'spring' as const,
            stiffness: 100,
            damping: 15,
        },
    },
};

export function FeaturesSection() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, margin: '-100px' });

    return (
        <section className="relative min-h-screen bg-gradient-to-b from-slate-950 to-black py-24 overflow-hidden">
            {/* Background Spotlight Effect */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-500/10 rounded-full blur-[120px]" />
                <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-500/5 rounded-full blur-[100px]" />
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-pink-500/5 rounded-full blur-[100px]" />
            </div>

            {/* Floating Particles Background */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                {[...Array(20)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute w-1 h-1 bg-white/20 rounded-full"
                        initial={{
                            x: typeof window !== 'undefined' ? Math.random() * window.innerWidth : 0,
                            y: typeof window !== 'undefined' ? Math.random() * window.innerHeight : 0,
                            scale: Math.random() * 0.5 + 0.5,
                        }}
                        animate={{
                            y: [null as any, Math.random() * -200 - 100],
                            opacity: [0, 1, 0],
                        }}
                        transition={{
                            duration: Math.random() * 3 + 2,
                            repeat: Infinity,
                            delay: Math.random() * 2,
                            ease: 'linear',
                        }}
                    />
                ))}
            </div>

            {/* Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={isInView ? { opacity: 1, scale: 1 } : {}}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="inline-flex items-center gap-2 px-4 py-2 mb-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-full text-sm text-white/80"
                    >
                        <Sparkles className="w-4 h-4 text-purple-400" />
                        <span>Powered by AI</span>
                    </motion.div>

                    <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
                        <span className="block">Intelligence that</span>
                        <span className="block bg-gradient-to-r from-purple-400 via-pink-500 to-purple-600 bg-clip-text text-transparent">
                            understands you
                        </span>
                    </h2>

                    <p className="text-xl text-slate-400 max-w-2xl mx-auto">
                        Experience the next generation of task management with AI that learns from your behavior
                    </p>
                </motion.div>

                {/* Floating Glass Tiles Grid */}
                <motion.div
                    ref={ref}
                    variants={containerVariants}
                    initial="hidden"
                    animate={isInView ? 'visible' : 'hidden'}
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
                >
                    {features.map((feature, index) => (
                        <FeatureCard key={index} feature={feature} index={index} />
                    ))}
                </motion.div>
            </div>
        </section>
    );
}

// Separate FeatureCard component for cleaner code
function FeatureCard({ feature, index }: { feature: Feature; index: number }) {
    const Icon = feature.icon;

    return (
        <motion.div
            variants={cardVariants}
            whileHover={{
                y: -10,
                transition: { type: 'spring' as const, stiffness: 300, damping: 20 }
            }}
            className="group relative"
        >
            {/* Hover Glow Effect */}
            <motion.div
                className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
                initial={{ scale: 0.8 }}
                whileHover={{ scale: 1.1 }}
            />

            {/* Glass Tile */}
            <div className="relative h-full bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-[0_8px_32px_rgba(0,0,0,0.4)] group-hover:border-white/20 transition-all duration-300">

                {/* Icon Container */}
                <motion.div
                    whileHover={{
                        scale: 1.1,
                        rotate: [0, -5, 5, -5, 0],
                    }}
                    transition={{ duration: 0.5 }}
                    className={`relative w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 group-hover:shadow-[0_0_30px_rgba(168,85,247,0.3)] transition-shadow`}
                >
                    {/* Pulsing Background */}
                    <motion.div
                        className="absolute inset-0 rounded-2xl bg-white/10"
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.5, 0.8, 0.5],
                        }}
                        transition={{
                            duration: 2,
                            repeat: Infinity,
                            ease: 'easeInOut',
                        }}
                    />

                    <Icon className="relative w-8 h-8 text-white z-10" />
                </motion.div>

                {/* Content */}
                <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-purple-300 transition-colors">
                    {feature.title}
                </h3>

                <p className="text-slate-400 leading-relaxed group-hover:text-slate-300 transition-colors">
                    {feature.description}
                </p>

                {/* Decorative Corner Elements */}
                <div className="absolute top-3 right-3 w-2 h-2 rounded-full bg-white/20 group-hover:bg-purple-400/50 transition-colors" />
                <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full bg-white/20 group-hover:bg-purple-400/50 transition-colors" />
            </div>
        </motion.div>
    );
}
