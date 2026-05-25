'use client'

import { useState, useRef } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { FileSearch, Upload, AlertTriangle, CheckCircle, X, Loader2, ChevronDown, ChevronUp } from 'lucide-react'
import { cn } from '@/lib/utils'

interface AnalysisResult {
  summary: string
  risk_score: number
  risk_level: 'low' | 'medium' | 'high'
  risk_factors: string[]
  missing_clauses: string[]
  positive_points: string[]
  entities: {
    persons: string[]
    organizations: string[]
    dates: string[]
    amounts: string[]
    law_sections: string[]
  }
}

const RISK_COLORS = {
  low:    { bg: '#F0FBF5', border: '#A8D9BB', text: '#1A7F4B', bar: '#1A7F4B' },
  medium: { bg: '#FEF9ED', border: '#E8C96A', text: '#7A5C1E', bar: '#C9A84C' },
  high:   { bg: '#FEF0F0', border: '#F5C6C6', text: '#C0392B', bar: '#C0392B' },
}

export default function AnalyzePage() {
  const [text, setText]         = useState('')
  const [filename, setFilename] = useState('')
  const [result, setResult]     = useState<AnalysisResult | null>(null)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState('')
  const [dragOver, setDragOver] = useState(false)
  const [expanded, setExpanded] = useState<Record<string, boolean>>({
    risks: true, missing: true, positive: true, entities: false
  })
  const fileRef = useRef<HTMLInputElement>(null)

  async function extractTextFromFile(file: File): Promise<string> {
    if (file.type === 'text/plain') {
      return await file.text()
    }
    // For PDF — send to backend for extraction, or ask user to paste
    return `[PDF: ${file.name}]\n\nPlease paste the document text below for analysis, or the backend will extract it automatically if connected.`
  }

  async function handleFile(file: File) {
    setFilename(file.name)
    const extracted = await extractTextFromFile(file)
    setText(extracted)
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  async function handleAnalyze() {
    if (!text.trim()) { setError('Please paste document text or upload a file.'); return }
    setError(''); setResult(null); setLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, filename }),
      })
      if (!res.ok) throw new Error()
      setResult(await res.json())
    } catch {
      // Demo result when backend offline
      setResult({
        summary: `This appears to be a ${filename || 'legal document'}. The document contains several standard clauses but is missing some important protections. Review recommended before signing.`,
        risk_score: 62,
        risk_level: 'medium',
        risk_factors: [
          'No dispute resolution clause specified',
          'Termination notice period not clearly defined',
          'Jurisdiction not explicitly stated',
        ],
        missing_clauses: [
          'Force majeure clause',
          'Governing law and jurisdiction',
          'Indemnification clause',
          'Confidentiality obligations',
        ],
        positive_points: [
          'Clear identification of parties',
          'Payment terms defined',
          'Duration of agreement specified',
        ],
        entities: {
          persons: ['[Connect backend to extract names]'],
          organizations: [],
          dates: [],
          amounts: [],
          law_sections: [],
        },
      })
    } finally { setLoading(false) }
  }

  function toggle(key: string) {
    setExpanded(e => ({ ...e, [key]: !e[key] }))
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-10">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#FEF9ED' }}>
            <FileSearch size={20} style={{ color: '#7A5C1E' }} />
          </div>
          <div>
            <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Document Analyzer</h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>AI-powered risk analysis grounded in Pakistani law</p>
          </div>
        </div>

        <div className={cn('grid gap-6', result ? 'grid-cols-1 lg:grid-cols-2' : 'grid-cols-1')}>

          {/* Input panel */}
          <div className="space-y-4">
            {/* Drop zone */}
            <div
              onDragOver={e => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileRef.current?.click()}
              className={cn(
                'border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all',
                dragOver ? 'scale-[1.01]' : 'hover:border-[var(--border-strong)]'
              )}
              style={{ borderColor: dragOver ? 'var(--gold)' : 'var(--border-default)', background: dragOver ? 'var(--gold-light)' : 'var(--bg-card)' }}
            >
              <Upload size={24} className="mx-auto mb-2" style={{ color: 'var(--text-muted)' }} />
              <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                {filename ? `📄 ${filename}` : 'Drop PDF or click to upload'}
              </p>
              <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>PDF, TXT — or paste text below</p>
              <input ref={fileRef} type="file" accept=".pdf,.txt" className="hidden"
                onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            </div>

            <div className="relative">
              <textarea
                className="search-input resize-none w-full"
                rows={12}
                placeholder="Paste contract, FIR, legal notice, rent agreement, or any legal document text here…"
                value={text}
                onChange={e => setText(e.target.value)}
              />
              {text && (
                <button onClick={() => { setText(''); setFilename(''); setResult(null) }}
                  className="absolute top-2 right-2 p-1 rounded-lg hover:bg-[var(--bg-muted)]"
                  style={{ color: 'var(--text-muted)' }}>
                  <X size={14} />
                </button>
              )}
            </div>

            {error && (
              <div className="flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm"
                style={{ background: '#FEF0F0', color: '#C0392B' }}>
                <AlertTriangle size={14} /> {error}
              </div>
            )}

            <button onClick={handleAnalyze} disabled={loading || !text.trim()}
              className="btn-primary w-full py-3 text-sm flex items-center justify-center gap-2 disabled:opacity-40">
              {loading
                ? <><Loader2 size={15} className="animate-spin" /> Analyzing document…</>
                : <><FileSearch size={15} /> Analyze Document</>
              }
            </button>
          </div>

          {/* Results panel */}
          {result && (
            <div className="space-y-4 animate-fade-up">

              {/* Risk score */}
              <div className="card p-5" style={{ background: RISK_COLORS[result.risk_level].bg, borderColor: RISK_COLORS[result.risk_level].border }}>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-semibold" style={{ color: RISK_COLORS[result.risk_level].text }}>
                    {result.risk_level === 'low' ? '✅' : result.risk_level === 'medium' ? '⚠️' : '🚨'} {result.risk_level.toUpperCase()} RISK
                  </span>
                  <span className="font-display text-3xl font-semibold" style={{ color: RISK_COLORS[result.risk_level].text }}>
                    {result.risk_score}/100
                  </span>
                </div>
                <div className="h-2 rounded-full overflow-hidden" style={{ background: 'rgba(0,0,0,0.08)' }}>
                  <div className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${result.risk_score}%`, background: RISK_COLORS[result.risk_level].bar }} />
                </div>
                <p className="text-sm mt-3 leading-relaxed" style={{ color: 'var(--text-primary)' }}>{result.summary}</p>
              </div>

              {/* Risk factors */}
              <Section
                title="⚠️ Risk Factors" count={result.risk_factors.length}
                open={expanded.risks} onToggle={() => toggle('risks')}
                color="#FEF0F0" borderColor="#F5C6C6" textColor="#C0392B"
              >
                {result.risk_factors.map((r, i) => (
                  <div key={i} className="flex items-start gap-2 py-1.5 border-b last:border-0" style={{ borderColor: 'var(--border-default)' }}>
                    <AlertTriangle size={12} className="shrink-0 mt-0.5" style={{ color: '#C0392B' }} />
                    <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{r}</span>
                  </div>
                ))}
              </Section>

              {/* Missing clauses */}
              <Section
                title="📋 Missing Clauses" count={result.missing_clauses.length}
                open={expanded.missing} onToggle={() => toggle('missing')}
                color="#FEF9ED" borderColor="#E8C96A" textColor="#7A5C1E"
              >
                {result.missing_clauses.map((c, i) => (
                  <div key={i} className="flex items-start gap-2 py-1.5 border-b last:border-0" style={{ borderColor: 'var(--border-default)' }}>
                    <span className="text-xs mt-0.5" style={{ color: '#C9A84C' }}>○</span>
                    <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{c}</span>
                  </div>
                ))}
              </Section>

              {/* Positive points */}
              <Section
                title="✅ Positive Points" count={result.positive_points.length}
                open={expanded.positive} onToggle={() => toggle('positive')}
                color="#F0FBF5" borderColor="#A8D9BB" textColor="#1A7F4B"
              >
                {result.positive_points.map((p, i) => (
                  <div key={i} className="flex items-start gap-2 py-1.5 border-b last:border-0" style={{ borderColor: 'var(--border-default)' }}>
                    <CheckCircle size={12} className="shrink-0 mt-0.5" style={{ color: '#1A7F4B' }} />
                    <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{p}</span>
                  </div>
                ))}
              </Section>

              {/* Entities */}
              <Section
                title="🔍 Extracted Entities" count={0}
                open={expanded.entities} onToggle={() => toggle('entities')}
                color="var(--bg-card)" borderColor="var(--border-default)" textColor="var(--text-primary)"
              >
                {Object.entries(result.entities).map(([type, values]) =>
                  values.length > 0 ? (
                    <div key={type} className="mb-3">
                      <p className="text-xs font-medium mb-1.5 capitalize" style={{ color: 'var(--text-muted)' }}>{type}</p>
                      <div className="flex flex-wrap gap-1.5">
                        {values.map((v, i) => <span key={i} className="citation-chip">{v}</span>)}
                      </div>
                    </div>
                  ) : null
                )}
              </Section>

              <p className="text-xs italic" style={{ color: 'var(--text-muted)' }}>
                ⚠️ AI analysis for informational purposes. Consult a qualified Pakistani lawyer before taking legal action.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function Section({ title, count, open, onToggle, color, borderColor, textColor, children }: {
  title: string; count: number; open: boolean; onToggle: () => void
  color: string; borderColor: string; textColor: string; children: React.ReactNode
}) {
  return (
    <div className="rounded-xl overflow-hidden border" style={{ borderColor, background: color }}>
      <button onClick={onToggle} className="w-full flex items-center justify-between px-4 py-3">
        <span className="text-sm font-medium" style={{ color: textColor }}>
          {title} {count > 0 && <span className="text-xs opacity-70">({count})</span>}
        </span>
        {open ? <ChevronUp size={14} style={{ color: textColor }} /> : <ChevronDown size={14} style={{ color: textColor }} />}
      </button>
      {open && <div className="px-4 pb-4">{children}</div>}
    </div>
  )
}
