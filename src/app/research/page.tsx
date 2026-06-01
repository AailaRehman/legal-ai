'use client'

import { useState, useEffect } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { BookOpen, Search, Loader2, ChevronRight, ChevronLeft, FileText, X } from 'lucide-react'
import { cn } from '@/lib/utils'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const LAW_ICONS: Record<string, string> = {
  'Constitution':   '🏛️',
  'Penal Code':     '⚖️',
  'Criminal Proc':  '🚔',
  'Electronic':     '💻',
  'Family':         '👨‍👩‍👧',
  'Contract':       '📝',
  'Transfer':       '🏠',
  'Shahadat':       '📋',
  'Income Tax':     '💰',
  'Rent':           '🏘️',
  'Industrial':     '🏭',
  'Consumer':       '🛒',
  'Terrorism':      '🛡️',
  'Narcotic':       '💊',
  'Companies':      '🏢',
  'Civil Servant':  '👔',
  'Laundering':     '🔍',
  'Child':          '👶',
  'Dissolution':    '💔',
  'Estacode':       '📚',
  'Land':           '🌍',
  'Mental':         '🧠',
  'Rules':          '📜',
  'West Pakistan':  '⚖️',
}

function getLawIcon(name: string) {
  for (const [key, icon] of Object.entries(LAW_ICONS)) {
    if (name.includes(key)) return icon
  }
  return '📄'
}

interface SearchResult {
  text: string
  source: string
  section: string
  score: number
}

interface BrowseChunk {
  text: string
  source: string
  section: string
}

function getToken() {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('mizan_token')
}

function authHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

export default function ResearchPage() {
  const [tab, setTab]               = useState<'search' | 'browse'>('search')
  const [laws, setLaws]             = useState<string[]>([])

  // Search state
  const [query, setQuery]           = useState('')
  const [lawFilter, setLawFilter]   = useState('')
  const [searchResults, setResults] = useState<SearchResult[]>([])
  const [searching, setSearching]   = useState(false)
  const [expanded, setExpanded]     = useState<number | null>(null)

  // Browse state
  const [selectedLaw, setSelectedLaw] = useState('')
  const [chunks, setChunks]           = useState<BrowseChunk[]>([])
  const [browsing, setBrowsing]       = useState(false)
  const [page, setPage]               = useState(1)
  const [total, setTotal]             = useState(0)
  const PAGE_SIZE = 8

  useEffect(() => { loadLaws() }, [])

  async function loadLaws() {
    try {
      const res = await fetch(`${API}/research/laws`, { headers: authHeaders() })
      if (res.ok) {
        const data = await res.json()
        setLaws(data.laws)
      }
    } catch {
      setLaws([
        'Constitution of Pakistan 1973', 'Pakistan Penal Code 1860',
        'Code Of Criminal Procedure', 'Prevention-Of-Electronic-Crime-Act-2016',
        'Muslim Family Laws Ordinance 1961', 'Contract Act 1872',
        'Transfer of Property Act 1882', 'Qanun-E-Shahadat Order 1984',
        'Income Tax Ordinance 2001', 'Rent Restriction Ordinance 1959',
        'Industrial Relations Act, 2012', 'Consumer Protection Act 2019',
        'Anti-Terrorism Act 1997', 'Control of Narcotic Substances Act 1997',
        'Companies Act 2017', 'Civil Servants Act, 1973',
        'Anti-Money Laundering (Aml) Act, 2010', 'Child Marriage Restraint Act',
        'Dissolution Of Muslim Marriages Act 1939', 'Estacode',
        'Land Aquisition Act', 'Mental Health Ordinance 2001',
        'Rules Of Business 1973', 'West Pakistan Family Courts Act 1964',
      ])
    }
  }

  async function handleSearch() {
    if (!query.trim()) return
    setResults([]); setSearching(true); setExpanded(null)
    try {
      const res = await fetch(`${API}/research/search`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ query, law_filter: lawFilter || null, k: 8 }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setResults(data.results)
    } catch {
      setResults([{
        text: 'Backend not connected or KB not built. Once running, semantic search across all 24 Pakistani law PDFs will appear here.',
        source: 'System', section: '', score: 0,
      }])
    } finally { setSearching(false) }
  }

  async function handleBrowse(law: string, p = 1) {
    setSelectedLaw(law); setChunks([]); setBrowsing(true); setPage(p)
    try {
      const res = await fetch(`${API}/research/browse`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ law_name: law, page: p, page_size: PAGE_SIZE }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setChunks(data.chunks)
      setTotal(data.total)
    } catch {
      setChunks([{ text: 'Could not load law content. Make sure backend is running.', source: law, section: '' }])
    } finally { setBrowsing(false) }
  }

  const totalPages = Math.ceil(total / PAGE_SIZE)

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-10">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#FEF0F0' }}>
            <BookOpen size={20} style={{ color: '#5C1A1A' }} />
          </div>
          <div>
            <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Law Research</h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Semantic search + browse across {laws.length} Pakistani law documents
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 rounded-lg mb-6 w-fit" style={{ background: 'var(--bg-muted)' }}>
          {[
            { key: 'search', label: '🔍 Search Laws' },
            { key: 'browse', label: '📚 Browse by Law' },
          ].map(({ key, label }) => (
            <button key={key} onClick={() => setTab(key as typeof tab)}
              className={cn('px-4 py-2 rounded-md text-sm font-medium transition-all', tab === key ? 'shadow-sm' : '')}
              style={{ background: tab === key ? 'var(--bg-card)' : 'transparent', color: tab === key ? 'var(--text-primary)' : 'var(--text-muted)' }}>
              {label}
            </button>
          ))}
        </div>

        {/* ── SEARCH TAB ── */}
        {tab === 'search' && (
          <div className="space-y-5">
            <div className="card p-5 space-y-3">
              <div className="flex gap-2">
                <div className="flex-1 relative">
                  <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: 'var(--text-muted)' }} />
                  <input
                    className="search-input pl-9 w-full"
                    placeholder='e.g. "punishment for theft" or "tenant eviction rights"'
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleSearch()}
                  />
                </div>
                <button onClick={handleSearch} disabled={searching || !query.trim()}
                  className="btn-primary px-5 text-sm flex items-center gap-2 disabled:opacity-40 shrink-0">
                  {searching ? <Loader2 size={14} className="animate-spin" /> : <Search size={14} />}
                  Search
                </button>
              </div>

              {/* Law filter chips */}
              <div>
                <p className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>Filter by law (optional):</p>
                <div className="flex flex-wrap gap-1.5">
                  <button onClick={() => setLawFilter('')}
                    className={cn('text-xs px-2.5 py-1 rounded-full transition-all')}
                    style={{
                      background: !lawFilter ? 'var(--navy)' : 'var(--bg-muted)',
                      color:      !lawFilter ? '#fff' : 'var(--text-secondary)',
                    }}>
                    All Laws
                  </button>
                  {laws.slice(0, 8).map(law => (
                    <button key={law} onClick={() => setLawFilter(lawFilter === law ? '' : law)}
                      className="text-xs px-2.5 py-1 rounded-full transition-all"
                      style={{
                        background: lawFilter === law ? 'var(--gold-light)' : 'var(--bg-muted)',
                        color:      lawFilter === law ? 'var(--warning)' : 'var(--text-secondary)',
                        border:     lawFilter === law ? '0.5px solid var(--gold-border)' : '0.5px solid var(--border-default)',
                      }}>
                      {getLawIcon(law)} {law.split(' ').slice(0, 3).join(' ')}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Results */}
            {searchResults.length > 0 && (
              <div className="space-y-3">
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  {searchResults.length} results for "{query}"
                  {lawFilter && ` in ${lawFilter}`}
                </p>
                {searchResults.map((r, i) => (
                  <div key={i} className="card overflow-hidden">
                    <button className="w-full flex items-start gap-3 p-4 text-left hover:bg-[var(--bg-muted)] transition-colors"
                      onClick={() => setExpanded(expanded === i ? null : i)}>
                      <span className="text-lg shrink-0 mt-0.5">{getLawIcon(r.source)}</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="citation-chip">{r.source}</span>
                          {r.section && <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{r.section}</span>}
                          <span className="text-xs ml-auto" style={{ color: 'var(--text-muted)' }}>
                            {Math.round((1 - r.score) * 100)}% match
                          </span>
                        </div>
                        <p className="text-sm leading-relaxed" style={{ color: 'var(--text-primary)' }}>
                          {expanded === i ? r.text : r.text.slice(0, 180) + (r.text.length > 180 ? '…' : '')}
                        </p>
                      </div>
                      <ChevronRight size={14} className={cn('shrink-0 mt-1 transition-transform', expanded === i ? 'rotate-90' : '')}
                        style={{ color: 'var(--text-muted)' }} />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {!searching && searchResults.length === 0 && query && (
              <div className="card p-8 text-center">
                <p className="text-sm" style={{ color: 'var(--text-muted)' }}>No results found. Try a different query.</p>
              </div>
            )}
          </div>
        )}

        {/* ── BROWSE TAB ── */}
        {tab === 'browse' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

            {/* Law list */}
            <div className="card p-3 h-fit">
              <p className="text-xs font-medium px-2 mb-2" style={{ color: 'var(--text-muted)' }}>
                SELECT A LAW ({laws.length})
              </p>
              <div className="space-y-0.5 max-h-[600px] overflow-y-auto">
                {laws.map(law => (
                  <button key={law} onClick={() => handleBrowse(law, 1)}
                    className={cn('w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-left transition-all')}
                    style={{
                      background: selectedLaw === law ? 'var(--gold-light)' : 'transparent',
                      color:      selectedLaw === law ? 'var(--warning)' : 'var(--text-secondary)',
                    }}>
                    <span className="text-base shrink-0">{getLawIcon(law)}</span>
                    <span className="text-xs leading-tight">{law}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Chunks panel */}
            <div className="lg:col-span-2 space-y-3">
              {!selectedLaw && (
                <div className="card p-10 text-center">
                  <BookOpen size={28} className="mx-auto mb-3" style={{ color: 'var(--text-muted)' }} />
                  <p className="text-sm" style={{ color: 'var(--text-muted)' }}>Select a law from the left to browse its content</p>
                </div>
              )}

              {browsing && (
                <div className="card p-8 text-center">
                  <Loader2 size={20} className="animate-spin mx-auto mb-2" style={{ color: 'var(--gold)' }} />
                  <p className="text-sm" style={{ color: 'var(--text-muted)' }}>Loading {selectedLaw}…</p>
                </div>
              )}

              {!browsing && chunks.length > 0 && (
                <>
                  <div className="flex items-center justify-between">
                    <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                      {selectedLaw} · {total} sections · page {page}/{totalPages}
                    </p>
                  </div>

                  {chunks.map((chunk, i) => (
                    <div key={i} className="card p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <FileText size={12} style={{ color: 'var(--text-muted)' }} />
                        <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{chunk.section}</span>
                      </div>
                      <p className="text-sm leading-relaxed" style={{ color: 'var(--text-primary)' }}>{chunk.text}</p>
                    </div>
                  ))}

                  {/* Pagination */}
                  {totalPages > 1 && (
                    <div className="flex items-center justify-center gap-2 pt-2">
                      <button onClick={() => handleBrowse(selectedLaw, page - 1)} disabled={page === 1}
                        className="p-2 rounded-lg disabled:opacity-30 hover:bg-[var(--bg-muted)] transition-colors"
                        style={{ color: 'var(--text-secondary)' }}>
                        <ChevronLeft size={16} />
                      </button>
                      <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                        {page} / {totalPages}
                      </span>
                      <button onClick={() => handleBrowse(selectedLaw, page + 1)} disabled={page === totalPages}
                        className="p-2 rounded-lg disabled:opacity-30 hover:bg-[var(--bg-muted)] transition-colors"
                        style={{ color: 'var(--text-secondary)' }}>
                        <ChevronRight size={16} />
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
