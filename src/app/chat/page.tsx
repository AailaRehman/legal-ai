'use client'

import { useEffect, useRef, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { Scale } from 'lucide-react'
import { Navbar }        from '@/components/layout/Navbar'
import { ChatSidebar }   from '@/components/chat/ChatSidebar'
import { ChatMessage }   from '@/components/chat/ChatMessage'
import { ChatInput }     from '@/components/chat/ChatInput'
import { ThemeToggle }   from '@/components/ui/ThemeToggle'
import { useChat }       from '@/hooks/useChat'

const EMPTY_PROMPTS = [
  { emoji: '🏠', label: 'Tenant rights',        q: 'What are my rights as a tenant in Pakistan?' },
  { emoji: '🚔', label: 'Arrest rights',        q: 'What are my rights if I am arrested without a warrant?' },
  { emoji: '📄', label: 'FIR procedure',        q: 'How do I file an FIR in Pakistan?' },
  { emoji: '💼', label: 'Contract breach',      q: 'What can I do if someone breaches a contract?' },
  { emoji: '🔒', label: 'Cybercrime PECA',      q: 'What does PECA 2016 say about cybercrime?' },
  { emoji: '👨‍👩‍👧', label: 'Family law',         q: 'How does divorce work under Muslim Family Laws Ordinance 1961?' },
]

function ChatPageInner() {
  const searchParams = useSearchParams()
  const bottomRef    = useRef<HTMLDivElement>(null)

  const {
    messages, isLoading, mode, setMode,
    sendMessage, clearChat, stopGeneration,
  } = useChat()

  // Handle ?q= from landing page search
  useEffect(() => {
    const q = searchParams.get('q')
    const m = searchParams.get('mode') as 'citizen' | 'lawyer' | 'student' | null
    if (m) setMode(m)
    if (q) sendMessage(q)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const isEmpty = messages.length === 0

  return (
    <div className="h-screen flex flex-col overflow-hidden" style={{ background: 'var(--bg-page)' }}>
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar — hidden on mobile */}
        <div className="hidden md:flex">
          <ChatSidebar
            mode={mode}
            setMode={setMode}
            onNew={clearChat}
            onClear={clearChat}
            msgCount={messages.length}
          />
        </div>

        {/* Main chat area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top bar */}
          <div
            className="flex items-center justify-between px-4 py-2 border-b shrink-0"
            style={{ borderColor: 'var(--border-default)', background: 'var(--bg-card)' }}
          >
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                Legal Chat
              </span>
              <span className={`mode-badge mode-${mode}`}>{mode}</span>
            </div>
            <ThemeToggle />
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
            {isEmpty ? (
              <EmptyState onSelect={sendMessage} mode={mode} />
            ) : (
              <>
                {messages.map((msg, i) => (
                  <ChatMessage
                    key={i}
                    message={msg}
                    isStreaming={isLoading && i === messages.length - 1 && msg.role === 'assistant'}
                  />
                ))}
                {isLoading && messages[messages.length - 1]?.role !== 'assistant' && (
                  <TypingIndicator />
                )}
              </>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <ChatInput
            onSend={sendMessage}
            onStop={stopGeneration}
            isLoading={isLoading}
            mode={mode}
          />
        </div>
      </div>
    </div>
  )
}

function EmptyState({ onSelect, mode }: { onSelect: (q: string) => void; mode: string }) {
  return (
    <div className="max-w-2xl mx-auto w-full pt-8 animate-fade-up">
      <div className="text-center mb-10">
        <div
          className="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4"
          style={{ background: 'var(--navy)' }}
        >
          <Scale size={22} color="#C9A84C" />
        </div>
        <h2 className="font-display text-2xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
          Ask Mizan anything
        </h2>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Legal intelligence grounded in Pakistani law · {mode} mode
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {EMPTY_PROMPTS.map(({ emoji, label, q }) => (
          <button
            key={label}
            onClick={() => onSelect(q)}
            className="card flex items-center gap-3 px-4 py-3 text-left hover:shadow-sm transition-all hover:-translate-y-0.5 duration-150"
          >
            <span className="text-xl shrink-0">{emoji}</span>
            <div>
              <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{label}</p>
              <p className="text-xs leading-snug mt-0.5" style={{ color: 'var(--text-muted)' }}>{q}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex gap-3 items-start">
      <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style={{ background: 'var(--navy)' }}>
        <Scale size={14} color="#C9A84C" />
      </div>
      <div
        className="flex items-center gap-1.5 px-4 py-3 rounded-2xl rounded-tl-sm"
        style={{ background: 'var(--chat-ai-bg)' }}
      >
        <div className="typing-dot" />
        <div className="typing-dot" />
        <div className="typing-dot" />
      </div>
    </div>
  )
}

export default function ChatPage() {
  return (
    <Suspense>
      <ChatPageInner />
    </Suspense>
  )
}
