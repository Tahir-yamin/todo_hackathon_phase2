'use client';

import { useState, useEffect, useRef } from 'react';
import { useSession } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Send, MessageSquare, Sparkles, ArrowLeft, Home } from 'lucide-react';

interface Message {
    role: 'user' | 'model';
    content: string;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [conversationId, setConversationId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const { data: session } = useSession();
    const router = useRouter();

    useEffect(() => {
        if (!session) {
            router.push('/auth');
        }
    }, [session, router]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || !session) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const token = localStorage.getItem('auth_token');
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${session.user.id}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    message: userMessage
                })
            });

            const data = await response.json();

            if (!conversationId) {
                setConversationId(data.conversation_id);
            }

            setMessages(prev => [...prev, { role: 'model', content: data.response }]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, {
                role: 'model',
                content: '❌ Sorry, I encountered an error. Please try again.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-screen bg-background-dark">
            {/* Header */}
            <div className="cyber-panel px-6 py-4 border-b border-border-subtle">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <Sparkles className="w-6 h-6 text-primary" />
                        <div>
                            <h1 className="text-2xl font-bold text-primary font-mono">AI Task Assistant</h1>
                            <p className="text-sm text-text-dark">Powered by Google Gemini • Manage tasks with natural language</p>
                        </div>
                    </div>
                    <Link
                        href="/"
                        className="flex items-center gap-2 px-4 py-2 bg-background-medium hover:bg-background-light border border-border-subtle rounded-sm transition-colors group"
                    >
                        <Home className="w-5 h-5 text-text-dark group-hover:text-primary" />
                        <span className="text-sm font-medium text-text-dark group-hover:text-primary">Back to Tasks</span>
                    </Link>
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
                <div className="max-w-4xl mx-auto space-y-4">
                    {messages.length === 0 && (
                        <div className="text-center py-12">
                            <MessageSquare className="w-16 h-16 text-primary mx-auto mb-4 opacity-50" />
                            <h2 className="text-xl font-semibold text-text-light mb-2">Start a conversation</h2>
                            <p className="text-text-dark mb-6">Try asking me to:</p>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                                <button
                                    onClick={() => setInput('Add a task to buy groceries')}
                                    className="cyber-panel p-3 text-left hover:border-primary transition-colors"
                                >
                                    <span className="text-primary">→</span> Add a task to buy groceries
                                </button>
                                <button
                                    onClick={() => setInput('Show me all my tasks')}
                                    className="cyber-panel p-3 text-left hover:border-primary transition-colors"
                                >
                                    <span className="text-primary">→</span> Show me all my tasks
                                </button>
                                <button
                                    onClick={() => setInput('What tasks are pending?')}
                                    className="cyber-panel p-3 text-left hover:border-primary transition-colors"
                                >
                                    <span className="text-primary">→</span> What tasks are pending?
                                </button>
                                <button
                                    onClick={() => setInput('Mark task 1 as complete')}
                                    className="cyber-panel p-3 text-left hover:border-primary transition-colors"
                                >
                                    <span className="text-primary">→</span> Mark task 1 as complete
                                </button>
                            </div>
                        </div>
                    )}

                    {messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] p-4 rounded-lg ${msg.role === 'user'
                                    ? 'bg-primary text-background-dark font-medium'
                                    : 'cyber-panel'
                                    }`}
                            >
                                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="flex justify-start">
                            <div className="cyber-panel p-4">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input */}
            <div className="cyber-panel p-6 border-t border-border-subtle">
                <div className="max-w-4xl mx-auto flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask me to manage your tasks..."
                        className="flex-1 cyber-input px-4 py-3 text-base"
                        disabled={loading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !input.trim()}
                        className="px-6 py-3 bg-primary text-background-dark rounded-sm font-medium hover:shadow-glow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        <Send className="w-5 h-5" />
                        <span className="hidden sm:inline">Send</span>
                    </button>
                </div>
                <p className="text-xs text-text-dark text-center mt-3">
                    Tip: Press Enter to send, Shift+Enter for new line
                </p>
            </div>
        </div>
    );
}
