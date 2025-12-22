'use client';

import { useState, useEffect, useRef } from 'react';
import { useSession } from '@/lib/auth-client';
import { Send, MessageSquare, X, Minimize2, Sparkles } from 'lucide-react';

interface Message {
    role: 'user' | 'model';
    content: string;
}

export function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [conversationId, setConversationId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const { data: session } = useSession();

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
            // Use real session user ID - call Railway backend
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${session.user.id}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
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

            // Auto-refresh if task was created
            if (data.response && (data.response.toLowerCase().includes('created') || data.response.toLowerCase().includes('added'))) {
                setTimeout(() => window.location.reload(), 2000);
            }
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

    if (!session) return null;

    return (
        <>
            {/* Chat Widget Container */}
            {isOpen && (
                <div className="fixed bottom-24 right-6 w-96 h-[600px] bg-[#0a0f1a] border border-cyan-500/30 rounded-lg shadow-2xl flex flex-col z-[9999]" style={{ backgroundColor: '#0a0f1a' }}>
                    {/* Header */}
                    <div className="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border-subtle rounded-t-lg">
                        <div className="flex items-center gap-2">
                            <Sparkles className="w-5 h-5 text-primary" />
                            <div>
                                <h3 className="font-bold text-sm text-primary">AI Assistant</h3>
                                <p className="text-xs text-text-dark">Powered by Gemini</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-1 hover:bg-background-light rounded transition-colors"
                                title="Minimize"
                            >
                                <Minimize2 className="w-4 h-4 text-text-dark hover:text-primary" />
                            </button>
                            <button
                                onClick={() => {
                                    setIsOpen(false);
                                    setMessages([]);
                                }}
                                className="p-1 hover:bg-background-light rounded transition-colors"
                                title="Close"
                            >
                                <X className="w-4 h-4 text-text-dark hover:text-red-500" />
                            </button>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 custom-scrollbar" style={{ backgroundColor: '#0d1520' }}>
                        {messages.length === 0 && (
                            <div className="text-center py-8">
                                <MessageSquare className="w-12 h-12 text-primary/30 mx-auto mb-3" />
                                <p className="text-sm text-text-dark mb-4">Ask me to manage your tasks!</p>
                                <div className="space-y-2">
                                    <button
                                        onClick={() => setInput('Add a task to buy groceries')}
                                        className="w-full text-left p-2 text-xs bg-background-medium hover:bg-background-light border border-border-subtle rounded transition-colors"
                                    >
                                        <span className="text-primary">→</span> Add a task
                                    </button>
                                    <button
                                        onClick={() => setInput('Show me all my tasks')}
                                        className="w-full text-left p-2 text-xs bg-background-medium hover:bg-background-light border border-border-subtle rounded transition-colors"
                                    >
                                        <span className="text-primary">→</span> Show tasks
                                    </button>
                                </div>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`mb-3 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[85%] p-3 rounded-lg text-sm ${msg.role === 'user'
                                        ? 'bg-primary text-background-dark'
                                        : 'bg-background-medium border border-border-subtle text-text-light'
                                        }`}
                                >
                                    <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                                </div>
                            </div>
                        ))}

                        {loading && (
                            <div className="flex justify-start mb-3">
                                <div className="bg-background-medium border border-border-subtle p-3 rounded-lg">
                                    <div className="flex space-x-1">
                                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-3 border-t border-cyan-500/30 rounded-b-lg" style={{ backgroundColor: '#0a0f1a' }}>
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask me anything..."
                                className="flex-1 px-3 py-2 border border-cyan-500/30 rounded text-sm text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400 transition-colors"
                                style={{ backgroundColor: '#1a2332' }}
                                disabled={loading}
                            />
                            <button
                                onClick={sendMessage}
                                disabled={loading || !input.trim()}
                                className="px-4 py-2 bg-primary text-background-dark rounded font-medium hover:shadow-glow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                        <p className="text-[10px] text-text-dark mt-1 text-center">Press Enter to send</p>
                    </div>
                </div>
            )}

            {/* Chat Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-br from-primary to-secondary rounded-full shadow-2xl hover:shadow-glow transition-all hover:scale-110 flex items-center justify-center z-50 group"
                title="AI Chat Assistant"
            >
                {isOpen ? (
                    <X className="w-6 h-6 text-background-dark" />
                ) : (
                    <>
                        <MessageSquare className="w-6 h-6 text-background-dark animate-pulse" />
                        {messages.length === 0 && (
                            <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-background-dark animate-ping"></span>
                        )}
                    </>
                )}
            </button>
        </>
    );
}
