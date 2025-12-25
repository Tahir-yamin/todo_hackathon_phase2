'use client';

import { motion } from 'framer-motion';
import { Twitter, Linkedin, Sparkles } from 'lucide-react';
import Link from 'next/link';

export function Footer() {
    return (
        <footer className="relative bg-black border-t border-white/10 py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">

                    {/* Logo & Tagline */}
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 
                flex items-center justify-center">
                                <Sparkles className="w-5 h-5 text-white" />
                            </div>
                            <span className="text-white font-bold text-xl">TaskFlow AI</span>
                        </div>
                        <p className="text-slate-400 text-sm">
                            Your AI-powered productivity engine
                        </p>
                    </div>

                    {/* Social Links */}
                    <div className="flex justify-center gap-4">
                        {[
                            { icon: Linkedin, href: 'https://linkedin.com/in/tahiryamin', label: 'LinkedIn' },
                            { icon: Twitter, href: 'https://twitter.com/tahir_yamin_', label: 'Twitter' },
                        ].map((social) => (
                            <motion.a
                                key={social.label}
                                href={social.href}
                                target="_blank"
                                rel="noopener noreferrer"
                                whileHover={{ scale: 1.1, y: -2 }}
                                whileTap={{ scale: 0.95 }}
                                className="w-10 h-10 rounded-full bg-white/5 border border-white/10 
                  flex items-center justify-center hover:bg-white/10 
                  hover:border-purple-500/50 transition-all group"
                                aria-label={social.label}
                            >
                                <social.icon className="w-5 h-5 text-slate-400 group-hover:text-white transition-colors" />
                            </motion.a>
                        ))}
                    </div>

                    {/* CTA Link */}
                    <div className="text-center md:text-right">
                        <Link
                            href="/auth"
                            className="inline-flex items-center gap-2 px-6 py-3 
                bg-gradient-to-r from-purple-600 to-pink-600 rounded-full 
                text-white font-semibold hover:shadow-lg hover:shadow-purple-500/50 
                transition-all"
                        >
                            <span>Get Started</span>
                            <Sparkles className="w-4 h-4" />
                        </Link>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="mt-8 pt-8 border-t border-white/10 text-center">
                    <p className="text-slate-500 text-sm">
                        © {new Date().getFullYear()} TaskFlow AI. Built for{' '}
                        <span className="text-purple-400">Panaversity Hackathon Phase 3</span>
                    </p>
                </div>
            </div>
        </footer>
    );
}
