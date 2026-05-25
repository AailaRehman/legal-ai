'use client'

import { Scale, User, Copy, Check } from 'lucide-react'
import { useState } from 'react'
import type { ChatMessage as ChatMessageType } from '@/lib/api'
import { cn } from '@/lib/utils'

interface Props {
  message: ChatMessageType
  isStreaming?: boolean
}

export function ChatMessage({ message, isStreaming }: Props) {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'

  async function copyText() {
    await navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <div className={cn('flex gap-3 group', isUser && 'flex-row-reverse')}>
      {/* Avatar */}
      <div
        className={cn(
          'w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5',
          isUser ? 'bg-[var(--bg-muted)]' : ''
        )}
        style={!isUser ? { background: 'var(--navy)' } : undefined}
      >
        {isUser
          ? <User size={14} style={{ color: 'var(--text-secondary)' }} />
          : <Scale size={14} color="#C9A84C" />
        }
      </div>

      <div className={cn('flex flex-col gap-2 max-w-[78%]', isUser && 'items-end')}>
        {/* Bubble */}
        <div
          className={cn(
            'px-4 py-3 rounded-2xl text-sm leading-relaxed',
            isUser
              ? 'rounded-tr-sm'
              : 'rounded-tl-sm'
          )}
          style={{
            background: isUser ? 'var(--chat-user-bg)' : 'var(--chat-ai-bg)',
            color:      isUser ? 'var(--chat-user-fg)' : 'var(--chat-ai-fg)',
            whiteSpace: 'pre-wrap',
          }}
        >
          {message.content}
          {isStreaming && (
            <span
              className="inline-block w-1.5 h-4 ml-0.5 animate-pulse rounded-sm align-middle"
              style={{ background: 'var(--gold)' }}
            />
          )}
        </div>

        {/* Citations */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-1.5 px-1">
            <span className="text-xs" style={{ color: 'var(--text-muted)' }}>Sources:</span>
            {message.sources.map((src, i) => (
              <span key={i} className="citation-chip">
                {src.law} · {src.section}
              </span>
            ))}
          </div>
        )}

        {/* Copy button */}
        {!isUser && !isStreaming && message.content && (
          <button
            onClick={copyText}
            className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 text-xs px-2 py-1 rounded-md"
            style={{ color: 'var(--text-muted)', background: 'var(--bg-muted)' }}
          >
            {copied ? <Check size={11} /> : <Copy size={11} />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        )}

        {/* Timestamp */}
        {message.timestamp && (
          <span className="text-[10px] px-1" style={{ color: 'var(--text-muted)' }}>
            {new Date(message.timestamp).toLocaleTimeString('en-PK', {
              hour: '2-digit', minute: '2-digit'
            })}
          </span>
        )}
      </div>
    </div>
  )
}
