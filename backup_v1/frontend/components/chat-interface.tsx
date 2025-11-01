'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Bot, User, Sparkles } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { cn } from '@/lib/utils';
import type { ChatMessage } from '@/lib/types';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
  initialMessage?: string;
  currentKey?: string | null;
  currentValue?: string | null;
}

export function ChatInterface({
  messages,
  onSendMessage,
  isLoading = false,
  disabled = false,
  initialMessage,
  currentKey,
  currentValue,
}: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (initialMessage && messages.length === 0) {
      inputRef.current?.focus();
    }
  }, [initialMessage, messages.length]);

  useEffect(() => {
    if (currentKey === undefined) return;
    setInput((currentValue ?? '').toString());
  }, [currentKey, currentValue]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || disabled) return;

    onSendMessage(input.trim());
    setInput('');
    
    // Keep focus on input field after submission for better UX
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  const formatMessage = (content: string): string => {
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br />');
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900 overflow-hidden">
      {/* HEADER - AI Assistant Title */}
      <div className="border-b border-slate-200/50 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm flex-shrink-0">
        <div className="p-3">
          <div className="flex items-center gap-2">
            <div className="rounded-full p-1.5 shadow-sm bg-primary/10 text-primary">
              <Sparkles className="h-3 w-3" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-xs font-bold text-slate-900 dark:text-slate-100">AI Assistant</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Instant guidance</p>
            </div>
          </div>
        </div>
      </div>

      {/* MESSAGES - SCROLLABLE AREA */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden scrollbar-hide p-3 bg-slate-50/30 dark:bg-slate-900 min-h-0">
        <div className="space-y-3">
          {/* Show initial message */}
          {messages.length === 0 && initialMessage && (
            <div className="flex gap-2 animate-fadeIn">
              <div className="rounded-full bg-primary/10 p-1.5 h-fit flex-shrink-0">
                <Bot className="h-3 w-3 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <div
                  className="text-xs rounded-lg bg-white dark:bg-slate-800 backdrop-blur-sm p-2 text-slate-700 dark:text-slate-200 leading-relaxed shadow-sm border border-slate-200/50 dark:border-slate-700 transition-all duration-300 hover:shadow-md"
                  dangerouslySetInnerHTML={{ __html: formatMessage(initialMessage) }}
                />
              </div>
            </div>
          )}

          {/* Show all messages with proper scrolling */}
          {messages.map((message, idx) => (
            <div
              key={message.id}
              className={cn(
                'flex gap-2 animate-fadeIn',
                message.role === 'user' && 'flex-row-reverse'
              )}
              style={{
                animationDelay: `${idx * 50}ms`,
              }}
            >
              <div
                className={cn(
                  'rounded-full p-1.5 h-fit flex-shrink-0 shadow-sm transition-all duration-200',
                  message.role === 'user'
                    ? 'bg-primary text-white'
                    : 'bg-primary/10 text-primary'
                )}
              >
                {message.role === 'user' ? (
                  <User className="h-3 w-3" />
                ) : (
                  <Bot className="h-3 w-3" />
                )}
              </div>
              <div
                className={cn(
                  'flex-1 rounded-lg p-2 text-xs leading-relaxed max-w-[85%] transition-all duration-300 shadow-sm border',
                  message.role === 'user'
                    ? 'bg-white text-slate-900 border-primary/30 ml-auto hover:shadow-md'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-slate-200/50 dark:border-slate-700 hover:shadow-md hover:border-slate-300/50'
                )}
              >
                <div
                  className="prose prose-xs max-w-none"
                  dangerouslySetInnerHTML={{ __html: formatMessage(message.content) }}
                />
              </div>
            </div>
          ))}

          {/* Loading State */}
          {isLoading && (
            <div className="flex gap-2 animate-fadeIn">
              <div className="rounded-full bg-primary/10 p-1.5 h-fit flex-shrink-0">
                <Bot className="h-3 w-3 text-primary" />
              </div>
              <div className="flex-1">
                <div className="rounded-lg bg-white p-2 flex items-center gap-2 shadow-sm border border-slate-200/50">
                  <div className="flex gap-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-primary/60 animate-bounce" style={{animationDelay: '0ms'}} />
                    <div className="h-1.5 w-1.5 rounded-full bg-primary/60 animate-bounce" style={{animationDelay: '150ms'}} />
                    <div className="h-1.5 w-1.5 rounded-full bg-primary/60 animate-bounce" style={{animationDelay: '300ms'}} />
                  </div>
                  <span className="text-xs text-slate-600">Analyzing...</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* INPUT BOX - AT BOTTOM */}
      <div className="border-t border-slate-200/50 dark:border-slate-800 p-3 bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm flex-shrink-0">
        <form onSubmit={handleSubmit} className="flex gap-2 group">
          <Input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your answer..."
            disabled={isLoading || disabled}
            className="text-sm h-9 rounded-xl bg-white dark:bg-slate-800 border-slate-200/60 dark:border-slate-700 transition-all duration-300 focus:border-primary/50 focus:shadow-md focus:ring-0 placeholder:text-slate-400 dark:placeholder:text-slate-500 shadow-sm text-slate-900 dark:text-slate-100"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <Button
            type="submit"
            disabled={!input.trim() || isLoading || disabled}
            className="h-9 px-3 flex-shrink-0 rounded-xl bg-primary hover:shadow-md transition-all duration-200 disabled:opacity-50 shadow-sm"
          >
            {isLoading ? (
              <Loader2 className="h-3 w-3 animate-spin" />
            ) : (
              <Send className="h-3 w-3" />
            )}
          </Button>
        </form>
      </div>
    </div>
  );
}