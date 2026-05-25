'use client'

import { useState } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { GraduationCap, Loader2, CheckCircle, XCircle, ChevronDown, BookOpen, Scale } from 'lucide-react'
import { cn } from '@/lib/utils'

const LEGAL_TOPICS: Record<string, string[]> = {
  'Constitutional Law': ['Fundamental Rights', 'Powers of Parliament', 'Judiciary', 'Emergency Powers', 'Constitutional Amendments'],
  'Criminal Law (PPC)': ['Offences Against Person', 'Property Offences', 'Defamation', 'Public Order', 'Cyber Crimes'],
  'Criminal Procedure (CrPC)': ['Arrest & Bail', 'FIR & Investigation', 'Trial Procedure', 'Appeals', 'Evidence'],
  'Civil Law': ['Contract Law', 'Property Law', 'Tort Law', 'Family Law', 'Succession'],
  'Family Law': ['Marriage & Divorce', 'Khula', 'Child Custody', 'Inheritance', 'Maintenance'],
  'Cyber Law (PECA 2016)': ['Cybercrime Offences', 'Data Protection', 'Online Content', 'Digital Forensics', 'Penalties'],
  'Labour Law': ['Employment Contract', 'Termination', 'Worker Rights', 'Industrial Disputes', 'Social Security'],
}

const LEVELS = ['student', 'citizen', 'lawyer'] as const
type Level = typeof LEVELS[number]

interface MCQ {
  question: string
  options: Record<string, string>
  correct: string
  explanation: string
}

interface CaseScenario {
  scenario: string
  question: string
  key_issues: string[]
  applicable_laws: string[]
  model_answer: string
  difficulty: string
}

export default function EducationPage() {
  const [tab, setTab] = useState<'mcq' | 'concept' | 'scenario'>('mcq')

  // MCQ state
  const [topic, setTopic]         = useState(Object.keys(LEGAL_TOPICS)[0])
  const [subtopic, setSubtopic]   = useState(LEGAL_TOPICS[Object.keys(LEGAL_TOPICS)[0]][0])
  const [numQ, setNumQ]           = useState(5)
  const [mcqs, setMcqs]           = useState<MCQ[]>([])
  const [answers, setAnswers]     = useState<Record<number, string>>({})
  const [submitted, setSubmitted] = useState(false)
  const [mcqLoading, setMcqLoading] = useState(false)

  // Concept state
  const [concept, setConcept]     = useState('')
  const [level, setLevel]         = useState<Level>('student')
  const [explanation, setExpl]    = useState('')
  const [conceptLoading, setConceptLoading] = useState(false)

  // Scenario state
  const [scenTopic, setScentopic]   = useState(Object.keys(LEGAL_TOPICS)[0])
  const [scenario, setScenario]     = useState<CaseScenario | null>(null)
  const [scenLoading, setScenLoading] = useState(false)
  const [showAnswer, setShowAnswer] = useState(false)

  // ── MCQ generation ─────────────────────────────────────────
  async function generateMCQs() {
    setMcqs([]); setAnswers({}); setSubmitted(false); setMcqLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/education/mcqs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, subtopic, num_questions: numQ }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setMcqs(data.questions)
    } catch {
      // Demo fallback MCQs
      setMcqs([
        {
          question: `Under the Constitution of Pakistan, which Article guarantees the right to a fair trial?`,
          options: { A: 'Article 9', B: 'Article 10A', C: 'Article 14', D: 'Article 19' },
          correct: 'B',
          explanation: 'Article 10A was inserted by the 18th Amendment and guarantees the right to a fair trial and due process.',
        },
        {
          question: 'Under Section 154 CrPC, a police officer is legally bound to register an FIR when a cognizable offence is reported.',
          options: { A: 'True — must register immediately', B: 'False — officer has discretion', C: 'True — but only for serious offences', D: 'False — needs court permission' },
          correct: 'A',
          explanation: 'Under Section 154 CrPC, registration of FIR is mandatory for cognizable offences. Police cannot refuse.',
        },
      ])
    } finally { setMcqLoading(false) }
  }

  function score() {
    return mcqs.filter((q, i) => answers[i] === q.correct).length
  }

  // ── Concept explainer ──────────────────────────────────────
  async function explainConcept() {
    if (!concept.trim()) return
    setExpl(''); setConceptLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/education/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ concept, level }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setExpl(data.explanation)
    } catch {
      setExpl(`[Backend not connected — preview]\n\n📖 Explanation of "${concept}" for ${level} level:\n\nOnce the FastAPI backend is running, this will provide a detailed, ${level}-appropriate explanation with Pakistani law references, examples, and key sections.`)
    } finally { setConceptLoading(false) }
  }

  // ── Case scenario ──────────────────────────────────────────
  async function getScenario() {
    setScenario(null); setShowAnswer(false); setScenLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/education/scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: scenTopic }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setScenario(data)
    } catch {
      setScenario({
        scenario: `Ali has been working at a private company for 5 years. His employer suddenly terminates him without giving any notice or severance pay, citing "restructuring". Ali has no written employment contract but has been receiving a regular salary.`,
        question: 'What are Ali\'s legal rights, and what remedies are available under Pakistani labour law?',
        key_issues: ['Wrongful termination', 'Notice period requirements', 'Severance pay entitlement', 'Labour court jurisdiction'],
        applicable_laws: ['Industrial and Commercial Employment (Standing Orders) Ordinance 1968', 'West Pakistan Industrial Disputes Act 1969', 'Workmen Compensation Act'],
        model_answer: 'Ali is entitled to notice pay or payment in lieu under Standing Orders Ordinance. He can file a complaint before the Labour Court within 30 days. Even without a written contract, his 5 years of continuous service creates entitlements to severance and benefits.',
        difficulty: 'Medium',
      })
    } finally { setScenLoading(false) }
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-10">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#F4EEF8' }}>
            <GraduationCap size={20} style={{ color: '#3A1A5C' }} />
          </div>
          <div>
            <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Legal Education</h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>MCQs, concept explainer, and case scenarios for Pakistani law</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 rounded-lg mb-6" style={{ background: 'var(--bg-muted)', width: 'fit-content' }}>
          {[
            { key: 'mcq',      label: '🎯 MCQ Quiz' },
            { key: 'concept',  label: '📖 Concept Explainer' },
            { key: 'scenario', label: '⚖️ Case Scenario' },
          ].map(({ key, label }) => (
            <button key={key} onClick={() => setTab(key as typeof tab)}
              className={cn('px-4 py-2 rounded-md text-sm font-medium transition-all', tab === key ? 'shadow-sm' : '')}
              style={{ background: tab === key ? 'var(--bg-card)' : 'transparent', color: tab === key ? 'var(--text-primary)' : 'var(--text-muted)' }}
            >
              {label}
            </button>
          ))}
        </div>

        {/* ── MCQ TAB ── */}
        {tab === 'mcq' && (
          <div className="space-y-5">
            <div className="card p-5 space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>Topic</label>
                  <div className="relative">
                    <select className="search-input appearance-none pr-8" value={topic}
                      onChange={e => { setTopic(e.target.value); setSubtopic(LEGAL_TOPICS[e.target.value][0]) }}>
                      {Object.keys(LEGAL_TOPICS).map(t => <option key={t}>{t}</option>)}
                    </select>
                    <ChevronDown size={13} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: 'var(--text-muted)' }} />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>Subtopic</label>
                  <div className="relative">
                    <select className="search-input appearance-none pr-8" value={subtopic} onChange={e => setSubtopic(e.target.value)}>
                      {LEGAL_TOPICS[topic].map(s => <option key={s}>{s}</option>)}
                    </select>
                    <ChevronDown size={13} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: 'var(--text-muted)' }} />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>Number of questions</label>
                  <div className="flex gap-2">
                    {[3, 5, 10].map(n => (
                      <button key={n} onClick={() => setNumQ(n)}
                        className={cn('flex-1 py-2 rounded-lg text-sm font-medium transition-all')}
                        style={{
                          background: numQ === n ? 'var(--navy)' : 'var(--bg-muted)',
                          color:      numQ === n ? '#fff' : 'var(--text-secondary)',
                        }}
                      >{n}</button>
                    ))}
                  </div>
                </div>
              </div>
              <button onClick={generateMCQs} disabled={mcqLoading}
                className="btn-primary px-6 py-2.5 text-sm flex items-center gap-2 disabled:opacity-50">
                {mcqLoading ? <><Loader2 size={14} className="animate-spin" />Generating…</> : '🎯 Generate Quiz'}
              </button>
            </div>

            {mcqs.length > 0 && (
              <div className="space-y-4">
                {mcqs.map((q, i) => (
                  <div key={i} className="card p-5">
                    <p className="text-sm font-medium mb-3" style={{ color: 'var(--text-primary)' }}>
                      <span className="citation-chip mr-2">Q{i + 1}</span>
                      {q.question}
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {Object.entries(q.options).map(([key, val]) => {
                        const selected  = answers[i] === key
                        const isCorrect = submitted && key === q.correct
                        const isWrong   = submitted && selected && key !== q.correct
                        return (
                          <button key={key} disabled={submitted}
                            onClick={() => setAnswers(a => ({ ...a, [i]: key }))}
                            className={cn('flex items-start gap-2.5 px-3 py-2.5 rounded-lg text-sm text-left transition-all border')}
                            style={{
                              background: isCorrect ? '#F0FBF5' : isWrong ? '#FEF0F0' : selected ? 'var(--gold-light)' : 'var(--bg-muted)',
                              borderColor: isCorrect ? '#A8D9BB' : isWrong ? '#F5C6C6' : selected ? 'var(--gold-border)' : 'var(--border-default)',
                              color: isCorrect ? '#1A7F4B' : isWrong ? '#C0392B' : 'var(--text-primary)',
                            }}
                          >
                            <span className="font-mono font-bold shrink-0">{key}.</span>
                            <span>{val}</span>
                            {isCorrect && <CheckCircle size={14} className="ml-auto shrink-0 mt-0.5" />}
                            {isWrong   && <XCircle    size={14} className="ml-auto shrink-0 mt-0.5" />}
                          </button>
                        )
                      })}
                    </div>
                    {submitted && (
                      <div className="mt-3 px-3 py-2.5 rounded-lg text-xs leading-relaxed"
                        style={{ background: 'var(--bg-muted)', color: 'var(--text-secondary)' }}>
                        <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>Explanation: </span>
                        {q.explanation}
                      </div>
                    )}
                  </div>
                ))}

                {!submitted ? (
                  <button onClick={() => setSubmitted(true)}
                    disabled={Object.keys(answers).length < mcqs.length}
                    className="btn-primary px-6 py-2.5 text-sm disabled:opacity-40">
                    Submit Answers
                  </button>
                ) : (
                  <div className="card p-5 text-center">
                    <p className="font-display text-3xl font-semibold mb-1" style={{ color: score() === mcqs.length ? '#1A7F4B' : 'var(--gold)' }}>
                      {score()} / {mcqs.length}
                    </p>
                    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                      {score() === mcqs.length ? '🎉 Perfect score!' : score() >= mcqs.length / 2 ? '👍 Good job!' : '📚 Keep studying!'}
                    </p>
                    <button onClick={() => { setMcqs([]); setAnswers({}); setSubmitted(false) }}
                      className="btn-ghost mt-3 text-sm px-4 py-2">
                      Try Again
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* ── CONCEPT TAB ── */}
        {tab === 'concept' && (
          <div className="space-y-5">
            <div className="card p-5 space-y-4">
              <div>
                <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                  Legal concept or term
                </label>
                <input className="search-input" placeholder='e.g. "Bail", "FIR", "Constitutional Petition", "Khula"'
                  value={concept} onChange={e => setConcept(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && explainConcept()} />
              </div>
              <div>
                <label className="block text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Explain for</label>
                <div className="flex gap-2">
                  {LEVELS.map(l => (
                    <button key={l} onClick={() => setLevel(l)}
                      className="flex-1 py-2 rounded-lg text-sm font-medium capitalize transition-all"
                      style={{
                        background: level === l ? 'var(--navy)' : 'var(--bg-muted)',
                        color:      level === l ? '#fff' : 'var(--text-secondary)',
                      }}>{l}</button>
                  ))}
                </div>
              </div>
              <button onClick={explainConcept} disabled={conceptLoading || !concept.trim()}
                className="btn-primary px-6 py-2.5 text-sm flex items-center gap-2 disabled:opacity-50">
                {conceptLoading ? <><Loader2 size={14} className="animate-spin" />Explaining…</> : <><BookOpen size={14} />Explain Concept</>}
              </button>
            </div>

            {explanation && (
              <div className="card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <BookOpen size={15} style={{ color: 'var(--gold)' }} />
                  <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                    {concept} — {level} level
                  </span>
                  <span className={cn('mode-badge ml-auto', `mode-${level}`)}>{level}</span>
                </div>
                <pre className="text-sm leading-relaxed whitespace-pre-wrap" style={{ fontFamily: 'DM Sans, sans-serif', color: 'var(--text-primary)' }}>
                  {explanation}
                </pre>
              </div>
            )}
          </div>
        )}

        {/* ── SCENARIO TAB ── */}
        {tab === 'scenario' && (
          <div className="space-y-5">
            <div className="card p-5 space-y-4">
              <div>
                <label className="block text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Topic area</label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {Object.keys(LEGAL_TOPICS).map(t => (
                    <button key={t} onClick={() => setScentopic(t)}
                      className={cn('px-3 py-2 rounded-lg text-xs text-left transition-all')}
                      style={{
                        background: scenTopic === t ? 'var(--gold-light)' : 'var(--bg-muted)',
                        color:      scenTopic === t ? 'var(--warning)' : 'var(--text-secondary)',
                        border:     scenTopic === t ? '0.5px solid var(--gold-border)' : '0.5px solid var(--border-default)',
                      }}>
                      {t}
                    </button>
                  ))}
                </div>
              </div>
              <button onClick={getScenario} disabled={scenLoading}
                className="btn-primary px-6 py-2.5 text-sm flex items-center gap-2 disabled:opacity-50">
                {scenLoading ? <><Loader2 size={14} className="animate-spin" />Loading…</> : <><Scale size={14} />Get Case Scenario</>}
              </button>
            </div>

            {scenario && (
              <div className="space-y-4">
                <div className="card p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>CASE SCENARIO</span>
                    <span className="citation-chip">{scenario.difficulty}</span>
                  </div>
                  <p className="text-sm leading-relaxed mb-4" style={{ color: 'var(--text-primary)' }}>{scenario.scenario}</p>
                  <div className="px-4 py-3 rounded-lg" style={{ background: 'var(--bg-muted)' }}>
                    <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>❓ {scenario.question}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="card p-4">
                    <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>KEY LEGAL ISSUES</p>
                    {scenario.key_issues.map((issue, i) => (
                      <div key={i} className="flex items-start gap-2 mb-1.5">
                        <span className="text-xs mt-0.5" style={{ color: 'var(--gold)' }}>•</span>
                        <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{issue}</span>
                      </div>
                    ))}
                  </div>
                  <div className="card p-4">
                    <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>APPLICABLE LAWS</p>
                    {scenario.applicable_laws.map((law, i) => (
                      <div key={i} className="citation-chip mb-1 inline-block mr-1">{law}</div>
                    ))}
                  </div>
                </div>

                <div className="card p-5">
                  {!showAnswer ? (
                    <button onClick={() => setShowAnswer(true)} className="btn-ghost text-sm px-4 py-2 w-full">
                      👁 Reveal Model Answer
                    </button>
                  ) : (
                    <div>
                      <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>MODEL ANSWER</p>
                      <p className="text-sm leading-relaxed" style={{ color: 'var(--text-primary)' }}>{scenario.model_answer}</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
