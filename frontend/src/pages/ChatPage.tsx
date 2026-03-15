import { useEffect, useRef, useState } from 'react';
import type { Message } from '../types/chat';
import { sendMessage } from '../services/chatService';
import { useChat } from '../contexts/ChatContext';
import { Trash2, ArrowUp, Briefcase, Code, GraduationCap } from 'lucide-react';
import PageTransition from '../components/PageTransition';
import avatar from '../assets/images/avatar.png';

export default function ChatPage() {
  const { messages, setMessages, clearChat } = useChat();
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    document.title = 'Chat — Hugo Carrasco';
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  useEffect(() => {
    if (!isLoading) inputRef.current?.focus();
  }, [isLoading]);

  const sendQuestion = async (question: string) => {
    if (!question || isLoading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: question,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendMessage(question);
      const aiMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.answer,
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = () => {
    const trimmed = input.trim();
    if (trimmed) sendQuestion(trimmed);
  };

  const suggestedQuestions = [
    {
      icon: <Briefcase className="size-4 text-brand" />,
      label: 'Work experience',
      question: "What is Hugo's professional experience?",
    },
    {
      icon: <Code className="size-4 text-brand" />,
      label: 'Tech stack',
      question: 'What technologies and tools does Hugo work with?',
    },
    {
      icon: <GraduationCap className="size-4 text-brand" />,
      label: 'Background',
      question: "What is Hugo's educational background?",
    },
  ];

  const handleSuggestionClick = (question: string) => {
    sendQuestion(question);
  };

  return (
    <PageTransition>
      <div className="flex flex-col h-[calc(100vh-theme(spacing.16)-theme(spacing.14))]">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4" aria-live="polite">
          <div className="max-w-3xl mx-auto space-y-4">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full gap-8 py-16">
                <div className="text-center">
                  <img
                    src={avatar}
                    alt="Hugo"
                    className="size-16 rounded-full object-cover mx-auto mb-4"
                  />
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                    Chat with Hugo's AI
                  </h2>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Ask me anything about Hugo's experience and projects.
                  </p>
                </div>
                <div className="grid gap-3 w-full max-w-md">
                  {suggestedQuestions.map((item) => (
                    <button
                      key={item.label}
                      onClick={() => handleSuggestionClick(item.question)}
                      className="flex items-center gap-3 px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-left hover:border-brand/50 hover:shadow-sm transition-all group"
                    >
                      <span className="flex items-center justify-center size-8 rounded-lg bg-brand/10 shrink-0">
                        {item.icon}
                      </span>
                      <div>
                        <p className="text-sm font-medium text-gray-900 dark:text-white group-hover:text-brand transition-colors">
                          {item.label}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">{item.question}</p>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
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
              <div className="flex items-start gap-3" aria-label="AI is typing">
                <img
                  src={avatar}
                  alt="Hugo"
                  className="size-12 rounded-full object-cover shrink-0 mt-1"
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
          <div className="max-w-3xl mx-auto flex items-center gap-2">
            {messages.length > 0 && (
              <button
                onClick={clearChat}
                title="Clear chat"
                className="size-10 flex items-center justify-center rounded-xl text-gray-400 hover:text-red-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors shrink-0"
              >
                <Trash2 className="size-4" />
              </button>
            )}
            <div className="relative flex-1">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleSend();
                }}
                autoFocus
                placeholder="Ask a question..."
                className="w-full pl-4 pr-12 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand"
              />
              <button
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="absolute right-2 top-1/2 -translate-y-1/2 size-8 flex items-center justify-center rounded-lg bg-brand text-white hover:opacity-90 transition-opacity disabled:opacity-30"
              >
                <ArrowUp className="size-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
