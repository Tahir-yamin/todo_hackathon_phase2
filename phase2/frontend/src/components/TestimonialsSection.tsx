'use client';

import { motion } from 'framer-motion';
import { Star } from 'lucide-react';

interface Testimonial {
    quote: string;
    author: string;
    role: string;
    avatar: string;
}

const testimonials: Testimonial[] = [
    {
        quote: "This AI completely transformed how I manage my day. I've never been this productive.",
        author: "Sarah Chen",
        role: "Product Manager",
        avatar: "SC",
    },
    {
        quote: "The neural analysis feature is insane. It knows what I need before I do.",
        author: "Marcus Rodriguez",
        role: "Software Engineer",
        avatar: "MR",
    },
    {
        quote: "Finally, a todo app that actually understands context. Game changer!",
        author: "Emily Watson",
        role: "Designer",
        avatar: "EW",
    },
    {
        quote: "I tried every productivity app. This is the only one powered by real AI.",
        author: "David Kim",
        role: "Founder",
        avatar: "DK",
    },
    {
        quote: "The smart sorting saves me hours every week. Absolutely worth it.",
        author: "Lisa Anderson",
        role: "Marketing Lead",
        avatar: "LA",
    },
];

// Duplicate for seamless loop
const duplicatedTestimonials = [...testimonials, ...testimonials];

export function TestimonialsSection() {
    return (
        <section className="relative bg-gradient-to-b from-slate-950 to-black py-24 overflow-hidden">
            {/* Background glow */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
          w-[600px] h-[600px] bg-purple-500/5 rounded-full blur-[100px]" />
            </div>

            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="text-center mb-16 px-4"
            >
                <h2 className="text-4xl sm:text-5xl font-bold text-white mb-4">
                    Loved by <span className="bg-gradient-to-r from-purple-400 to-pink-500 
            bg-clip-text text-transparent">thousands</span>
                </h2>
                <p className="text-slate-400 text-lg">
                    Join the productivity revolution
                </p>
            </motion.div>

            {/* Infinite Marquee */}
            <div className="relative">
                {/* Gradient Masks */}
                <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r 
          from-black to-transparent z-10 pointer-events-none" />
                <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l 
          from-black to-transparent z-10 pointer-events-none" />

                {/* Scrolling Container */}
                <motion.div
                    className="flex gap-6"
                    animate={{
                        x: [0, -50 * testimonials.length + '%'],
                    }}
                    transition={{
                        x: {
                            duration: 30,
                            repeat: Infinity,
                            ease: 'linear',
                        },
                    }}
                    whileHover={{ animationPlayState: 'paused' }}
                >
                    {duplicatedTestimonials.map((testimonial, index) => (
                        <TestimonialCard key={index} testimonial={testimonial} />
                    ))}
                </motion.div>
            </div>
        </section>
    );
}

function TestimonialCard({ testimonial }: { testimonial: Testimonial }) {
    return (
        <motion.div
            whileHover={{ y: -5, scale: 1.02 }}
            className="flex-shrink-0 w-[400px] group"
        >
            <div className="bg-white/5 backdrop-blur-md border border-white/10 
        rounded-3xl p-6 h-full group-hover:border-white/20 transition-all">

                {/* Stars */}
                <div className="flex gap-1 mb-4">
                    {[...Array(5)].map((_, i) => (
                        <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                </div>

                {/* Quote */}
                <p className="text-slate-300 mb-6 leading-relaxed">
                    "{testimonial.quote}"
                </p>

                {/* Author */}
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 
            flex items-center justify-center text-white font-semibold">
                        {testimonial.avatar}
                    </div>
                    <div>
                        <div className="text-white font-semibold">{testimonial.author}</div>
                        <div className="text-slate-400 text-sm">{testimonial.role}</div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
