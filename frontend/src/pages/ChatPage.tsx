import { useEffect, useRef, useState } from 'react';
import type { Message } from '../types/chat';
import { sendMessage } from '../services/chatService';
import avatar from '../assets/images/avatar.png';

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: trimmed,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendMessage(trimmed);
      const aiMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer,
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch {
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-theme(spacing.16)-theme(spacing.14))]">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.length === 0 ? (
            <p className="text-center text-gray-500 dark:text-gray-400 mt-8">
              Ask me anything about Hugo's experience and projects.
            </p>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {/* Avatar — só no assistant */}
                {msg.role === 'assistant' && (
                  <img
                    src={avatar}
                    alt="Hugo"
                    className="size-12 rounded-full object-cover shrink-0 mt-1"
                  />
                )}
                <div
                  className={`max-w-[75%] px-4 py-2 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-brand text-white'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))
          )}

          {/* Typing indicator */}
          {isLoading && (
            <div className="flex items-start gap-3">
              <img
                src={avatar}
                alt="Hugo"
                className="size-8 rounded-full object-cover shrink-0 mt-1"
              />
              <div className="bg-gray-100 dark:bg-gray-800 px-4 py-3 rounded-2xl">
                <div className="flex gap-1">
                  <span className="size-2 bg-gray-400 rounded-full animate-bounce" />
                  <span className="size-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.15s]" />
                  <span className="size-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.3s]" />
                </div>
              </div>
            </div>
          )}

          {/* Invisible element to scroll to */}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-4">
        <div className="max-w-3xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSend();
            }}
            placeholder="Ask a question..."
            className="flex-1 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-brand text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
