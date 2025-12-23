'use client';

import React, { useState } from 'react';
import { Sparkles, Loader2 } from 'lucide-react';

interface SmartTaskInputProps {
    onParse: (data: {
        title: string;
        due_date?: string | null;
        priority?: string;
        category?: string;
        tags?: string;
    }) => void;
}

export const SmartTaskInput: React.FC<SmartTaskInputProps> = ({ onParse }) => {
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleParse = async () => {
        if (!input.trim()) return;

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ai/parse-task`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ input_text: input })
            });

            if (!response.ok) {
                throw new Error('Failed to parse task');
            }

            const result = await response.json();

            if (result.success) {
                onParse(result.data);
                setInput('');
            } else {
                setError(result.message || 'Parsing failed');
            }
        } catch (err: any) {
            console.error('AI parsing failed:', err);
            setError(err.message || 'Failed to parse task');
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleParse();
        }
    };

    return (
        <div className="smart-input-container mb-6">
            <div className="relative">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="✨ Try: 'Buy groceries tomorrow at 5pm' or 'Urgent: Submit report by Friday'"
                    className="w-full px-4 py-3 pr-12 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    disabled={loading}
                />
                <button
                    onClick={handleParse}
                    disabled={loading || !input.trim()}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-purple-400 hover:text-purple-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    title="Parse with AI"
                >
                    {loading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                        <Sparkles className="w-5 h-5" />
                    )}
                </button>
            </div>

            {error && (
                <p className="text-xs text-red-400 mt-1">
                    {error}
                </p>
            )}

            <p className="text-xs text-slate-400 mt-1">
                💡 Use natural language - AI will parse it for you! Press Enter to parse.
            </p>
        </div>
    );
};
