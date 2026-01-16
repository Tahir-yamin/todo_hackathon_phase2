"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function AIChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Use relative path - Next.js rewrites will proxy to backend
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
      const response = await fetch(`${apiUrl}/api/hackathon-demo-user/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: input,
          conversation_history: messages.slice(-10).map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if new
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error("Chat error:", error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again."
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="ai-chat-container">
      <div className="chat-header">
        <h3>🤖 AI Task Assistant</h3>
        <p>Ask me to manage your tasks with natural language</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>👋 Hi! I can help you manage your tasks.</p>
            <p className="suggestions">Try saying:</p>
            <ul>
              <li>&quot;Add a task to call mom&quot;</li>
              <li>&quot;Show me all my tasks&quot;</li>
              <li>&quot;Mark my grocery task as complete&quot;</li>
            </ul>
          </div>
        )}

        {messages.map((m) => (
          <div key={m.id} className={`message ${m.role}`}>
            <div className="message-avatar">
              {m.role === "user" ? "👤" : "🤖"}
            </div>
            <div className="message-content">
              <strong>{m.role === "user" ? "You" : "AI Assistant"}</strong>
              <p>{m.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message... (e.g., 'Add a task to buy groceries')"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          {isLoading ? "..." : "Send"}
        </button>
      </form>

      <style jsx>{`
        .ai-chat-container {
          display: flex;
          flex-direction: column;
          height: 600px;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          background: white;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          overflow: hidden;
        }

        .chat-header {
          padding: 1.5rem;
          border-bottom: 1px solid #e5e7eb;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .chat-header h3 {
          margin: 0 0 0.5rem 0;
          font-size: 1.25rem;
          font-weight: 600;
        }

        .chat-header p {
          margin: 0;
          font-size: 0.875rem;
          opacity: 0.9;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 1.5rem;
          background: #f9fafb;
        }

        .empty-state {
          text-align: center;
          color: #6b7280;
          padding: 2rem;
        }

        .empty-state p {
          margin: 0.5rem 0;
        }

        .empty-state .suggestions {
          font-size: 0.875rem;
          font-weight: 600;
          margin-top: 1.5rem;
          margin-bottom: 0.5rem;
        }

        .empty-state ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .empty-state li {
          background: white;
          padding: 0.75rem;
          margin: 0.5rem 0;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
          cursor: pointer;
          transition: all 0.2s;
        }

        .empty-state li:hover {
          background: #f3f4f6;
          transform: translateX(4px);
        }

        .message {
          display: flex;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
          animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
          justify-content: flex-end;
        }

        .message.user .message-avatar {
          order: 2;
        }

        .message.user .message-content {
          text-align: right;
        }

        .message-avatar {
          font-size: 1.5rem;
          flex-shrink: 0;
        }

        .message-content {
          max-width: 70%;
          padding: 1rem;
          border-radius: 12px;
        }

        .message.user .message-content {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .message.assistant .message-content {
          background: white;
          border: 1px solid #e5e7eb;
          color: #111827;
        }

        .message-content strong {
          display: block;
          margin-bottom: 0.25rem;
          font-size: 0.875rem;
          opacity: 0.8;
        }

        .message-content p {
          margin: 0;
          line-height: 1.6;
        }

        .typing-indicator {
          display: flex;
          gap: 4px;
          padding: 0.5rem 0;
        }

        .typing-indicator span {
          display: block;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #9ca3af;
          animation: typing 1.4s infinite;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes typing {
          0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
          30% { transform: translateY(-10px); opacity: 1; }
        }

        .chat-input-form {
          display: flex;
          gap: 0.75rem;
          padding: 1.25rem;
          border-top: 1px solid #e5e7eb;
          background: white;
        }

        .chat-input-form input {
          flex: 1;
          padding: 0.875rem 1rem;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          font-size: 0.9375rem;
          transition: all 0.2s;
        }

        .chat-input-form input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .chat-input-form button {
          padding: 0.875rem 2rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: all 0.2s;
        }

        .chat-input-form button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .chat-input-form button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        /* Scrollbar styling */
        .chat-messages::-webkit-scrollbar {
          width: 8px;
        }

        .chat-messages::-webkit-scrollbar-track {
          background: #f1f1f1;
        }

        .chat-messages::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 4px;
        }

        .chat-messages::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }
      `}</style>
    </div>
  );
}
