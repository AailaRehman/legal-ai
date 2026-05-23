'use client'

import { Scale, Plus, Trash2, MessageSquare } from 'lucide-react'
import type { UserMode } from '@/lib/api'
import { cn } from '@/lib/utils'

interface Props {
  mode:      UserMode
  setMode:   (m: UserMode) => void
  onNew:     () => void
  onClear:   () => void
  msgCount:  number
}

const MODES: { value: UserMode; label: string; desc: string; emoji: string }[] = [
  { value: 'citizen', label: 'Citizen',  desc: 'Plain language',   emoji: '👤' },
  { value: 'lawyer',  label: 'Lawyer',   desc: 'Detailed & cited', emoji: '⚖️' },
  { value: 'student', label: 'Student',  desc: 'Educational',      emoji: '🎓' },
]

const SUGGESTED = [
  'Rights when arrested without a warrant',
  'How to file an FIR',
  'Tenant eviction law',
  'Cybercrime under PECA 2016',
  'Bail procedure in Pakistan',
  'Divorce under Muslim Family Law',
]

export function ChatSidebar({ mode, setMode, onNew, onClear, msgCount }: Props) {
  return (
    <aside
      className="w-64 shrink-0 flex flex-col border-r h-full"
      style={{ borderColor: 'var(--border-default)', background: 'var(--bg-card)' }}
    >
      {/* Logo */}
      <div className="p-4 border-b" style={{ borderColor: 'var(--border-default)' }}>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded flex items-center justify-center" style={{ background: 'var(--navy)' }}>
            <Scale size={12} color="#C9A84C" />
          </div>
          <span className="font-display font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>
            Mizan
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-5">
        {/* New chat */}
        <button
          onClick={onNew}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors hover:bg-[var(--bg-muted)]"
          style={{ color: 'var(--text-secondary)', border: '0.5px solid var(--border-default)' }}
        >
          <Plus size={14} />
          New conversation
        </button>

        {/* Mode selector */}
        <div>
          <p className="text-[10px] uppercase tracking-wider mb-2 px-1" style={{ color: 'var(--text-muted)' }}>
            Mode
          </p>
          <div className="space-y-1">
            {MODES.map(m => (
              <button
                key={m.value}
                onClick={() => setMode(m.value)}
                className={cn(
                  'w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors',
                  mode === m.value
                    ? 'bg-[var(--gold-light)] border-[0.5px] border-[var(--gold-border)]'
                    : 'hover:bg-[var(--bg-muted)]'
                )}
              >
                <span className="text-base">{m.emoji}</span>
                <div>
                  <p
                    className="text-xs font-medium"
                    style={{ color: mode === m.value ? 'var(--warning)' : 'var(--text-primary)' }}
                  >
                    {m.label}
                  </p>
                  <p className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
                    {m.desc}
                  </p>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Suggested queries */}
        <div>
          <p className="text-[10px] uppercase tracking-wider mb-2 px-1" style={{ color: 'var(--text-muted)' }}>
            Suggested
          </p>
          <div className="space-y-1">
            {SUGGESTED.map(q => (
              <button
                key={q}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left hover:bg-[var(--bg-muted)] transition-colors"
              >
                <MessageSquare size={11} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
                <span className="text-xs leading-tight" style={{ color: 'var(--text-secondary)' }}>
                  {q}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Footer actions */}
      {msgCount > 0 && (
        <div className="p-3 border-t" style={{ borderColor: 'var(--border-default)' }}>
          <button
            onClick={onClear}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs transition-colors hover:bg-[var(--bg-muted)]"
            style={{ color: 'var(--text-muted)' }}
          >
            <Trash2 size={12} />
            Clear conversation
          </button>
        </div>
      )}
    </aside>
  )
}
