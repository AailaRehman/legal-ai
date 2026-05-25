'use client'

import { useState } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { Scale, ChevronDown, Loader2, BookOpen, AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'

const URGENCY_LEVELS = ['Low — I have time to plan', 'Medium — Within days', 'High — Immediate crisis']
const RESOURCES = ['Limited (no lawyer budget)', 'Moderate (can hire a lawyer)', 'Good (full legal support)']
const ROLES_LIST = ['Complainant', 'Accused', 'Victim', 'Witness', 'Other Party']

const PROCEDURES = [
  'File an FIR', 'Apply for Bail', 'File a Civil Suit',
  'File a Constitutional Petition', 'Challenge a Court Order',
  'File a Consumer Complaint', 'Apply for Khula (Divorce)',
  'Register a Property',
]

export default function StrategyPage() {
  const [tab, setTab] = useState<'strategy' | 'procedure'>('strategy')

  // Strategy form
  const [situation, setSituation] = useState('')
  const [role, setRole]           = useState(ROLES_LIST[0])
  const [urgency, setUrgency]     = useState(URGENCY_LEVELS[1])
  const [resources, setResources] = useState(RESOURCES[0])
  const [result, setResult]       = useState('')
  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState('')

  // Procedure
  const [procedure, setProcedure]   = useState(PROCEDURES[0])
  const [procResult, setProcResult] = useState('')
  const [procLoading, setProcLoading] = useState(false)

  async function handleStrategy() {
    if (!situation.trim()) { setError('Please describe your legal situation.'); return }
    setError(''); setResult(''); setLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/strategy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ situation, role, urgency, resources }),
      })
      if (!res.ok) throw new Error('API error')
      const data = await res.json()
      setResult(data.strategy)
    } catch {
      setResult(`[Backend not connected — preview]\n\n## ⚖️ Legal Assessment\nYour situation has been noted. Once the FastAPI backend is running, you will receive a full 10-section legal strategy covering applicable laws, immediate actions, court procedures, required documents, timeline, and costs — all specific to Pakistani law.\n\nSituation entered: "${situation}"\nRole: ${role} | Urgency: ${urgency}`)
    } finally { setLoading(false) }
  }

  async function handleProcedure() {
    setProcResult(''); setProcLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/procedure', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ procedure }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setProcResult(data.procedure)
    } catch {
      setProcResult(`[Backend not connected — preview]\n\nStep-by-step guide for: **${procedure}**\n\nOnce FastAPI is running, this will show detailed steps, required documents, applicable law sections, fees, and timeframes specific to Pakistan.`)
    } finally { setProcLoading(false) }
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-10">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#EEF1F8' }}>
            <Scale size={20} style={{ color: 'var(--navy)' }} />
          </div>
          <div>
            <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Case Strategy</h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>AI-powered legal strategy grounded in Pakistani law</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 rounded-lg mb-6 w-fit" style={{ background: 'var(--bg-muted)' }}>
          {(['strategy', 'procedure'] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={cn('px-4 py-2 rounded-md text-sm font-medium transition-all', tab === t ? 'shadow-sm' : '')}
              style={{ background: tab === t ? 'var(--bg-card)' : 'transparent', color: tab === t ? 'var(--text-primary)' : 'var(--text-muted)' }}
            >
              {t === 'strategy' ? '⚖️ Get Strategy' : '📋 Court Procedures'}
            </button>
          ))}
        </div>

        {tab === 'strategy' && (
          <div className="space-y-5">
            <div className="card p-5 space-y-4">
              <div>
                <label className="block text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                  Describe your legal situation *
                </label>
                <textarea
                  className="search-input resize-none"
                  rows={5}
                  placeholder="e.g. My landlord has locked me out of my rented house without any court order. I have been living there for 3 years and have a written rent agreement. What should I do?"
                  value={situation}
                  onChange={e => setSituation(e.target.value)}
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <SelectField label="Your role" value={role} onChange={setRole} options={ROLES_LIST} />
                <SelectField label="Urgency" value={urgency} onChange={setUrgency} options={URGENCY_LEVELS} />
                <SelectField label="Resources" value={resources} onChange={setResources} options={RESOURCES} />
              </div>

              {error && (
                <div className="flex items-center gap-2 text-sm px-3 py-2 rounded-lg"
                  style={{ background: '#FEF0F0', color: '#C0392B' }}>
                  <AlertTriangle size={14} /> {error}
                </div>
              )}

              <button onClick={handleStrategy} disabled={loading}
                className="btn-primary px-6 py-2.5 text-sm flex items-center gap-2 disabled:opacity-50">
                {loading ? <><Loader2 size={14} className="animate-spin" /> Generating strategy…</> : '⚖️ Get Legal Strategy'}
              </button>
            </div>

            {result && <StrategyResult text={result} />}
          </div>
        )}

        {tab === 'procedure' && (
          <div className="space-y-5">
            <div className="card p-5 space-y-4">
              <div>
                <label className="block text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                  Select a legal procedure
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {PROCEDURES.map(p => (
                    <button key={p} onClick={() => setProcedure(p)}
                      className={cn('px-3 py-2.5 rounded-lg text-xs text-left transition-all', procedure === p ? 'ring-1' : '')}
                      style={{
                        background:   procedure === p ? 'var(--gold-light)' : 'var(--bg-muted)',
                        color:        procedure === p ? 'var(--warning)' : 'var(--text-secondary)',
                        border:       procedure === p ? '0.5px solid var(--gold-border)' : '0.5px solid var(--border-default)',
                      }}>
                      {p}
                    </button>
                  ))}
                </div>
              </div>
              <button onClick={handleProcedure} disabled={procLoading}
                className="btn-primary px-6 py-2.5 text-sm flex items-center gap-2 disabled:opacity-50">
                {procLoading ? <><Loader2 size={14} className="animate-spin" /> Loading…</> : '📋 Get Procedure Guide'}
              </button>
            </div>
            {procResult && (
              <div className="card p-6">
                <div className="prose prose-sm max-w-none" style={{ color: 'var(--text-primary)' }}>
                  <pre className="whitespace-pre-wrap text-sm leading-relaxed font-body" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                    {procResult}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function SelectField({ label, value, onChange, options }: {
  label: string; value: string; onChange: (v: string) => void; options: string[]
}) {
  return (
    <div>
      <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>{label}</label>
      <div className="relative">
        <select
          value={value}
          onChange={e => onChange(e.target.value)}
          className="search-input appearance-none pr-8 cursor-pointer"
        >
          {options.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
        <ChevronDown size={13} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: 'var(--text-muted)' }} />
      </div>
    </div>
  )
}

function StrategyResult({ text }: { text: string }) {
  const sections = text.split(/(?=##\s)/).filter(Boolean)
  return (
    <div className="card p-6 space-y-4">
      <div className="flex items-center gap-2 mb-2">
        <BookOpen size={16} style={{ color: 'var(--gold)' }} />
        <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>Legal Strategy Report</span>
      </div>
      {sections.length > 1 ? (
        sections.map((section, i) => {
          const lines   = section.trim().split('\n')
          const heading = lines[0].replace(/^##\s*/, '')
          const body    = lines.slice(1).join('\n').trim()
          return (
            <div key={i} className="border-l-2 pl-4 py-1" style={{ borderColor: 'var(--gold)' }}>
              <p className="text-sm font-semibold mb-1" style={{ color: 'var(--text-primary)' }}>{heading}</p>
              <p className="text-sm leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--text-secondary)' }}>{body}</p>
            </div>
          )
        })
      ) : (
        <pre className="text-sm leading-relaxed whitespace-pre-wrap" style={{ fontFamily: 'DM Sans, sans-serif', color: 'var(--text-primary)' }}>{text}</pre>
      )}
      <p className="text-xs italic mt-4" style={{ color: 'var(--text-muted)' }}>
        ⚠️ This is AI-generated legal strategy for informational purposes only. Consult a qualified Pakistani lawyer before taking any legal action.
      </p>
    </div>
  )
}
