'use client'

import { useState, useEffect } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { RequireAuth } from '@/components/auth/RequireAuth'
import { useAuth } from '@/contexts/AuthContext'
import { authHeaders } from '@/lib/auth.api'
import { LayoutDashboard, MessageSquare, FileSearch, Pen, Scale, Trash2, Clock, ChevronRight, Plus } from 'lucide-react'
import Link from 'next/link'
import { cn } from '@/lib/utils'

type DashTab = 'overview' | 'chats' | 'documents' | 'strategies'
const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function DashboardPage() {
  return <RequireAuth><DashboardInner /></RequireAuth>
}

function DashboardInner() {
  const { user } = useAuth()
  const [tab, setTab] = useState<DashTab>('overview')
  const [chats, setChats]         = useState<any[]>([])
  const [docs, setDocs]           = useState<any[]>([])
  const [strategies, setStrategies] = useState<any[]>([])

  useEffect(() => { loadData() }, [])

  async function loadData() {
    try {
      const [cRes, dRes, sRes] = await Promise.all([
        fetch(`${API}/user/chats`,      { headers: authHeaders() }),
        fetch(`${API}/user/documents`,  { headers: authHeaders() }),
        fetch(`${API}/user/strategies`, { headers: authHeaders() }),
      ])
      if (cRes.ok) setChats(await cRes.json())
      if (dRes.ok) setDocs(await dRes.json())
      if (sRes.ok) setStrategies(await sRes.json())
    } catch {
      setChats([
        { session_id: 'demo-1', title: 'Tenant eviction rights query', mode: 'citizen', created_at: new Date().toISOString(), message_count: 6 },
        { session_id: 'demo-2', title: 'Bail application procedure',   mode: 'lawyer',  created_at: new Date(Date.now()-86400000).toISOString(), message_count: 12 },
      ])
      setDocs([{ id: 1, title: 'Rent Agreement Review', doc_type: 'Rent Agreement', created_at: new Date().toISOString() }])
      setStrategies([{ id: 1, title: 'Wrongful termination case', situation: 'My employer fired me without notice...', created_at: new Date().toISOString() }])
    }
  }

  const STATS = [
    { label: 'Conversations', value: chats.length,      icon: MessageSquare, color: '#1A2744' },
    { label: 'Documents',     value: docs.length,       icon: FileSearch,    color: '#7A5C1E' },
    { label: 'Strategies',    value: strategies.length, icon: Scale,         color: '#1A5C35' },
    { label: 'Drafts',        value: 0,                 icon: Pen,           color: '#3A1A5C' },
  ]

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#EEF1F8' }}>
              <LayoutDashboard size={20} style={{ color: 'var(--navy)' }} />
            </div>
            <div>
              <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Dashboard</h1>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                Welcome back, <span style={{ color: 'var(--gold)' }}>{user?.username}</span>
              </p>
            </div>
          </div>
          <Link href="/chat" className="btn-primary text-sm px-4 py-2 flex items-center gap-2">
            <Plus size={14} /> New Chat
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          {STATS.map(({ label, value, icon: Icon, color }) => (
            <div key={label} className="card p-4 flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0" style={{ background: `${color}15` }}>
                <Icon size={16} style={{ color }} />
              </div>
              <div>
                <p className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>{value}</p>
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{label}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-1 p-1 rounded-lg mb-5 w-fit" style={{ background: 'var(--bg-muted)' }}>
          {[
            { key: 'overview',   label: '📊 Overview'  },
            { key: 'chats',      label: '💬 Chats'      },
            { key: 'documents',  label: '📄 Documents'  },
            { key: 'strategies', label: '⚖️ Strategies' },
          ].map(({ key, label }) => (
            <button key={key} onClick={() => setTab(key as DashTab)}
              className={cn('px-4 py-2 rounded-md text-sm font-medium transition-all', tab === key ? 'shadow-sm' : '')}
              style={{ background: tab === key ? 'var(--bg-card)' : 'transparent', color: tab === key ? 'var(--text-primary)' : 'var(--text-muted)' }}>
              {label}
            </button>
          ))}
        </div>

        {tab === 'overview' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              { title: 'Recent Chats', items: chats.slice(0,3),    icon: '💬', href: '/chat' },
              { title: 'Documents',    items: docs.slice(0,3),     icon: '📄', href: '/analyze' },
            ].map(({ title, items, icon, href }) => (
              <div key={title} className="card p-5">
                <div className="flex items-center justify-between mb-3">
                  <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{icon} {title}</p>
                  <Link href={href} className="text-xs flex items-center gap-1" style={{ color: 'var(--gold)' }}>View all <ChevronRight size={11} /></Link>
                </div>
                {items.length === 0
                  ? <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Nothing here yet</p>
                  : items.map((item: any, i: number) => (
                    <div key={i} className="flex items-center gap-2 py-1.5 border-b last:border-0" style={{ borderColor: 'var(--border-default)' }}>
                      <Clock size={11} style={{ color: 'var(--text-muted)' }} />
                      <span className="text-xs flex-1 truncate" style={{ color: 'var(--text-primary)' }}>{item.title || item.session_id}</span>
                    </div>
                  ))
                }
              </div>
            ))}
          </div>
        )}

        {tab === 'chats' && (
          <div className="space-y-2">
            {chats.length === 0
              ? <Empty icon="💬" text="No conversations yet" href="/chat" action="Start chatting" />
              : chats.map((c: any) => (
                <div key={c.session_id} className="card px-4 py-3 flex items-center gap-3">
                  <MessageSquare size={15} style={{ color: 'var(--text-muted)' }} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate" style={{ color: 'var(--text-primary)' }}>{c.title}</p>
                    <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{c.message_count} messages · {new Date(c.created_at).toLocaleDateString()}</p>
                  </div>
                  <span className={cn('mode-badge', `mode-${c.mode}`)}>{c.mode}</span>
                  <button onClick={() => setChats(x => x.filter(s => s.session_id !== c.session_id))}
                    className="p-1.5 rounded hover:bg-[var(--bg-muted)]" style={{ color: 'var(--text-muted)' }}>
                    <Trash2 size={13} />
                  </button>
                </div>
              ))
            }
          </div>
        )}

        {tab === 'documents' && (
          <div className="space-y-2">
            {docs.length === 0
              ? <Empty icon="📄" text="No documents analyzed" href="/analyze" action="Analyze a document" />
              : docs.map((d: any) => (
                <div key={d.id} className="card px-4 py-3 flex items-center gap-3">
                  <FileSearch size={15} style={{ color: 'var(--text-muted)' }} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate" style={{ color: 'var(--text-primary)' }}>{d.title}</p>
                    <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{d.doc_type} · {new Date(d.created_at).toLocaleDateString()}</p>
                  </div>
                  <span className="citation-chip">{d.doc_type}</span>
                  <button onClick={() => setDocs(x => x.filter(s => s.id !== d.id))}
                    className="p-1.5 rounded hover:bg-[var(--bg-muted)]" style={{ color: 'var(--text-muted)' }}>
                    <Trash2 size={13} />
                  </button>
                </div>
              ))
            }
          </div>
        )}

        {tab === 'strategies' && (
          <div className="space-y-2">
            {strategies.length === 0
              ? <Empty icon="⚖️" text="No strategies saved" href="/strategy" action="Get a strategy" />
              : strategies.map((s: any) => (
                <div key={s.id} className="card px-4 py-3 flex items-center gap-3">
                  <Scale size={15} style={{ color: 'var(--text-muted)' }} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate" style={{ color: 'var(--text-primary)' }}>{s.title}</p>
                    <p className="text-xs truncate" style={{ color: 'var(--text-muted)' }}>{s.situation}</p>
                  </div>
                  <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{new Date(s.created_at).toLocaleDateString()}</span>
                </div>
              ))
            }
          </div>
        )}
      </div>
    </div>
  )
}

function Empty({ icon, text, href, action }: { icon: string; text: string; href: string; action: string }) {
  return (
    <div className="card p-10 text-center">
      <p className="text-3xl mb-3">{icon}</p>
      <p className="text-sm mb-4" style={{ color: 'var(--text-muted)' }}>{text}</p>
      <Link href={href} className="btn-primary text-sm px-4 py-2 inline-flex items-center gap-2">
        {action} <ChevronRight size={13} />
      </Link>
    </div>
  )
}
