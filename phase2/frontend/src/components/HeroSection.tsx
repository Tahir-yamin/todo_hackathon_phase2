'use client';

import { motion } from 'framer-motion';
import { Sparkles, Zap, Brain, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export function HeroSection() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden 
      bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900">

            {/* Animated Background Blobs */}
            <div className="absolute inset-0">
                <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-500 rounded-full 
          mix-blend-multiply filter blur-3xl opacity-30 animate-blob" />
                <div className="absolute top-0 -right-4 w-96 h-96 bg-pink-500 rounded-full 
          mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000" />
                <div className="absolute -bottom-8 left-20 w-96 h-96 bg-blue-500 rounded-full 
          mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000" />
            </div>

            {/* Grid Pattern Overlay */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] 
        bg-[size:100px_100px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,black,transparent)]" />

            {/* Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center">

                    {/* Badge */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-white/5 
              backdrop-blur-sm border border-white/10 rounded-full text-sm text-white/80"
                    >
                        <Sparkles className="w-4 h-4 text-purple-400" />
                        <span>AI-Powered Task Management</span>
                        <span className="px-2 py-0.5 bg-gradient-to-r from-purple-500 to-pink-500 
              rounded-full text-xs font-semibold">Phase 3</span>
                    </motion.div>

                    {/* Main Headline */}
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6"
                    >
                        <span className="block text-white">Manage Tasks with</span>
                        <span className="block bg-gradient-to-r from-purple-400 via-pink-500 to-purple-600 
              bg-clip-text text-transparent">
                            Natural Language AI
                        </span>
                    </motion.h1>

                    {/* Subtitle */}
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="text-xl sm:text-2xl text-white/70 mb-12 max-w-3xl mx-auto"
                    >
                        Just tell our AI what you need to do. No clicking, no forms—
                        <span className="text-white font-semibold"> just conversation</span>.
                    </motion.p>

                    {/* Feature Pills */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="flex flex-wrap justify-center gap-4 mb-12"
                    >
                        {[
                            { icon: Brain, text: 'Smart AI Assistant' },
                            { icon: Zap, text: 'Instant Updates' },
                            { icon: Sparkles, text: 'Beautiful UI' },
                        ].map((feature, i) => (
                            <div key={i} className="flex items-center gap-2 px-4 py-2 bg-white/5 
                backdrop-blur-sm border border-white/10 rounded-full text-white/80 
                hover:bg-white/10 transition-colors cursor-default">
                                <feature.icon className="w-4 h-4" />
                                <span>{feature.text}</span>
                            </div>
                        ))}
                    </motion.div>

                    {/* CTA Buttons */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.4 }}
                        className="flex flex-col sm:flex-row gap-4 justify-center"
                    >
                        <Link href="/dashboard">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="group px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 
                  rounded-full text-white font-semibold shadow-2xl hover:shadow-purple-500/50 
                  transition-all flex items-center gap-2"
                            >
                                <span>Try Live Demo</span>
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </motion.button>
                        </Link>
                    </motion.div>

                    {/* Stats */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5, delay: 0.5 }}
                        className="mt-16 flex flex-wrap justify-center gap-8 text-center"
                    >
                        {[
                            { value: '5', label: 'AI Tools' },
                            { value: '<2s', label: 'Response Time' },
                            { value: '100%', label: 'Free & Open Source' },
                        ].map((stat, i) => (
                            <div key={i} className="min-w-[120px]">
                                <div className="text-3xl font-bold bg-gradient-to-r from-purple-400 
                  to-pink-500 bg-clip-text text-transparent">
                                    {stat.value}
                                </div>
                                <div className="text-sm text-white/60 mt-1">{stat.label}</div>
                            </div>
                        ))}
                    </motion.div>

                </div>
            </div>

            {/* Bottom Fade */}
            <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t 
        from-black to-transparent" />
        </section>
    );
}
