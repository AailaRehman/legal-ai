'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Square, Mic } from 'lucide-react'
import type { UserMode } from '@/lib/api'
import { cn } from '@/lib/utils'

interface Props {
  onSend:       (message: string) => void
  onStop:       () => void
  isLoading:    boolean
  mode:         UserMode
  disabled?:    boolean
}

const PLACEHOLDER: Record<UserMode, string> = {
  citizen: 'Ask a legal question in plain English or Urdu…',
  lawyer:  'Describe the legal issue for detailed analysis…',
  student: 'Ask about a law, case, or legal concept…',
}

export function ChatInput({ onSend, onStop, isLoading, mode, disabled }: Props) {
  const [input, setInput] = useState('')
  const textareaRef       = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 180) + 'px'
  }, [input])

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  function handleSend() {
    const trimmed = input.trim()
    if (!trimmed || isLoading || disabled) return
    onSend(trimmed)
    setInput('')
  }

  return (
    <div
      className="p-3 border-t"
      style={{ borderColor: 'var(--border-default)', background: 'var(--bg-card)' }}
    >
      <div
        className="flex items-end gap-2 rounded-xl p-2"
        style={{
          background: 'var(--bg-elevated)',
          border: '0.5px solid var(--border-default)',
        }}
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={PLACEHOLDER[mode]}
          disabled={disabled}
          rows={1}
          className="flex-1 bg-transparent outline-none resize-none text-sm leading-relaxed py-1 px-2"
          style={{
            color:       'var(--text-primary)',
            fontFamily:  'DM Sans, sans-serif',
            minHeight:   '36px',
          }}
        />

        <div className="flex items-center gap-1.5 shrink-0 pb-0.5">
          {/* Mode badge */}
          <span className={cn('mode-badge', `mode-${mode}`)}>
            {mode}
          </span>

          {isLoading ? (
            <button
              onClick={onStop}
              className="w-8 h-8 rounded-lg flex items-center justify-center transition-colors"
              style={{ background: '#FEF0F0', color: '#C0392B' }}
              title="Stop"
            >
              <Square size={14} fill="currentColor" />
            </button>
          ) : (
            <button
              onClick={handleSend}
              disabled={!input.trim() || disabled}
              className="w-8 h-8 rounded-lg flex items-center justify-center transition-opacity disabled:opacity-30"
              style={{ background: 'var(--navy)', color: '#fff' }}
              title="Send (Enter)"
            >
              <Send size={14} />
            </button>
          )}
        </div>
      </div>

      <p className="text-center text-[10px] mt-2" style={{ color: 'var(--text-muted)' }}>
        Mizan provides legal information, not advice. Shift+Enter for new line.
      </p>
    </div>
  )
}
