'use client';

import Link from 'next/link';
import { MessageSquare } from 'lucide-react';

export function ChatLink() {
    return (
        <Link
            href="/chat"
            className="flex items-center gap-2 px-4 py-2 text-text-dark hover:text-primary transition-colors group"
        >
            <MessageSquare className="w-5 h-5 group-hover:animate-pulse" />
            <span className="font-mono">AI Chat</span>
        </Link>
    );
}
