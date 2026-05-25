'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Search, ChevronDown } from 'lucide-react'

const QUICK_QUERIES = [
  'Can a landlord evict without court order?',
  'What is the bail procedure in Pakistan?',
  'Rights of an arrested person under CrPC',
  'How to file a cybercrime complaint PECA',
  'Divorce process under Muslim Family Law',
]

const MODES = [
  { value: 'citizen', label: 'Citizen', desc: 'Plain language answers' },
  { value: 'lawyer',  label: 'Lawyer',  desc: 'Legal citations & detail' },
  { value: 'student', label: 'Student', desc: 'Educational explanations' },
]

export function Hero() {
  const router = useRouter()
  const [query, setQuery] = useState('')
  const [mode, setMode] = useState('citizen')
  const [modeOpen, setModeOpen] = useState(false)

  const selectedMode = MODES.find(m => m.value === mode)!

  function handleAsk() {
    if (!query.trim()) return
    router.push(`/chat?q=${encodeURIComponent(query)}&mode=${mode}`)
  }

  return (
    <section className="relative overflow-hidden pt-20 pb-16 px-4">
      {/* Subtle background pattern */}
      <div
        className="absolute inset-0 opacity-[0.03] dark:opacity-[0.05]"
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, var(--navy) 1px, transparent 0)`,
          backgroundSize: '32px 32px',
        }}
      />

      {/* Gold accent blob */}
      <div
        className="absolute top-0 right-1/4 w-96 h-96 rounded-full opacity-[0.06] dark:opacity-[0.04] pointer-events-none"
        style={{
          background: 'radial-gradient(circle, #C9A84C 0%, transparent 70%)',
          filter: 'blur(40px)',
        }}
      />

      <div className="relative max-w-3xl mx-auto text-center">
        {/* Badge */}
        <div
          className="inline-flex items-center gap-2 text-xs px-3 py-1.5 rounded-full mb-6 animate-fade-in"
          style={{
            background: 'var(--gold-light)',
            color: 'var(--warning)',
            border: '0.5px solid var(--gold-border)',
          }}
        >
          <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
          Pakistan Legal AI · 25+ Laws · LLaMA 3.3-70B
        </div>

        {/* Headline */}
        <h1
          className="font-display text-5xl sm:text-6xl font-semibold leading-[1.1] mb-5 animate-fade-up"
          style={{ color: 'var(--text-primary)', animationDelay: '0.1s' }}
        >
          Legal intelligence
          <br />
          <span style={{ color: 'var(--gold)' }}>grounded in</span>
          <br />
          Pakistani law
        </h1>

        <p
          className="text-base sm:text-lg leading-relaxed mb-10 max-w-xl mx-auto animate-fade-up"
          style={{ color: 'var(--text-secondary)', animationDelay: '0.2s' }}
        >
          Ask questions, analyze documents, draft contracts — all grounded in the
          Constitution, PPC, CrPC, PECA, and 20+ more Pakistani laws.
        </p>

        {/* Search bar */}
        <div
          className="animate-fade-up flex flex-col sm:flex-row gap-2 p-2 rounded-xl mb-4 shadow-sm"
          style={{
            background: 'var(--bg-card)',
            border: '0.5px solid var(--border-default)',
            animationDelay: '0.3s',
          }}
        >
          <div className="flex flex-1 items-center gap-2 px-2">
            <Search size={16} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            <input
              className="flex-1 bg-transparent outline-none text-sm"
              style={{ color: 'var(--text-primary)', fontFamily: 'DM Sans, sans-serif' }}
              placeholder='e.g. "What are my rights if arrested without a warrant?"'
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleAsk()}
            />
          </div>

          {/* Mode selector */}
          <div className="relative shrink-0">
            <button
              onClick={() => setModeOpen(!modeOpen)}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--bg-muted)',
                color: 'var(--text-secondary)',
                border: '0.5px solid var(--border-default)',
              }}
            >
              <span className={`mode-badge mode-${mode}`}>{selectedMode.label}</span>
              <ChevronDown size={13} />
            </button>

            {modeOpen && (
              <div
                className="absolute right-0 top-full mt-1 w-48 rounded-xl shadow-lg z-10 overflow-hidden"
                style={{
                  background: 'var(--bg-elevated)',
                  border: '0.5px solid var(--border-default)',
                }}
              >
                {MODES.map(m => (
                  <button
                    key={m.value}
                    onClick={() => { setMode(m.value); setModeOpen(false) }}
                    className="w-full text-left px-4 py-3 flex flex-col gap-0.5 hover:bg-[var(--bg-muted)] transition-colors"
                  >
                    <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                      {m.label}
                    </span>
                    <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                      {m.desc}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>

          <button
            onClick={handleAsk}
            className="btn-primary px-5 py-2 text-sm shrink-0"
          >
            Ask Mizan →
          </button>
        </div>

        {/* Quick queries */}
        <div className="flex flex-wrap gap-2 justify-center animate-fade-up" style={{ animationDelay: '0.4s' }}>
          {QUICK_QUERIES.map(q => (
            <button
              key={q}
              onClick={() => { setQuery(q); }}
              className="text-xs px-3 py-1.5 rounded-full transition-colors hover:border-[var(--border-strong)]"
              style={{
                background: 'var(--bg-muted)',
                color: 'var(--text-secondary)',
                border: '0.5px solid var(--border-default)',
              }}
            >
              {q}
            </button>
          ))}
        </div>
      </div>
    </section>
  )
}
