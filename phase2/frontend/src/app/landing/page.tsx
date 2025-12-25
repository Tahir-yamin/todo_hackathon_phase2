'use client';

import { HeroSection } from '@/components/HeroSection';
import { FeaturesSection } from '@/components/FeaturesSection';
import { HowItWorksSection } from '@/components/HowItWorksSection';
import { InteractiveDemo } from '@/components/InteractiveDemo';
import { TestimonialsSection } from '@/components/TestimonialsSection';
import { Footer } from '@/components/Footer';

export default function LandingPage() {
    return (
        <main className="min-h-screen bg-slate-950 text-white overflow-x-hidden 
      selection:bg-purple-500/30">

            {/* 1. The Floating Command Center Hero */}
            <section className="relative z-50">
                <HeroSection />
            </section>

            {/* 2. The Floating Glass Tiles Features */}
            <section className="relative z-40">
                <FeaturesSection />
            </section>

            {/* 3. The Connected Intelligence Stream */}
            <section className="relative z-30">
                <HowItWorksSection />
            </section>

            {/* 4. The Interactive "Try It" Demo */}
            <section className="relative z-40">
                <InteractiveDemo />
            </section>

            {/* 5. Social Proof Testimonials */}
            <section className="relative z-20">
                <TestimonialsSection />
            </section>

            {/* 6. Footer */}
            <Footer />

        </main>
    );
}
