'use client'

import { useState, useEffect } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { RequireAuth } from '@/components/auth/RequireAuth'
import { authHeaders } from '@/lib/auth.api'
import { Shield, Users, MessageSquare, FileSearch, TrendingUp, Search } from 'lucide-react'
import { cn } from '@/lib/utils'
import { ROLES } from '@/lib/auth.types'
import type { UserRole } from '@/lib/auth.types'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface UserRecord { id: number; username: string; email: string; role: UserRole; created_at: string; is_active: boolean }
interface Analytics  { total_users: number; total_messages: number; total_documents: number; total_strategies: number; users_by_role: Record<string, number>; active_today: number }

export default function AdminPage() {
  return <RequireAuth requiredRole="admin"><AdminInner /></RequireAuth>
}

function AdminInner() {
  const [tab, setTab]             = useState<'analytics' | 'users'>('analytics')
  const [users, setUsers]         = useState<UserRecord[]>([])
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [search, setSearch]       = useState('')
  const [loading, setLoading]     = useState(false)

  useEffect(() => { loadAll() }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const [uRes, aRes] = await Promise.all([
        fetch(`${API}/admin/users`,     { headers: authHeaders() }),
        fetch(`${API}/admin/analytics`, { headers: authHeaders() }),
      ])
      if (uRes.ok) setUsers(await uRes.json())
      if (aRes.ok) setAnalytics(await aRes.json())
    } catch {
      setUsers([
        { id: 1, username: 'admin',    email: 'admin@mizan.ai',    role: 'admin',   created_at: new Date().toISOString(), is_active: true },
        { id: 2, username: 'lawyer1',  email: 'lawyer1@test.com',  role: 'lawyer',  created_at: new Date().toISOString(), is_active: true },
        { id: 3, username: 'student1', email: 'student1@test.com', role: 'student', created_at: new Date().toISOString(), is_active: true },
        { id: 4, username: 'citizen1', email: 'citizen1@test.com', role: 'citizen', created_at: new Date().toISOString(), is_active: true },
      ])
      setAnalytics({
        total_users: 4, total_messages: 0, total_documents: 0, total_strategies: 0,
        users_by_role: { admin: 1, lawyer: 1, student: 1, citizen: 1 },
        active_today: 1,
      })
    } finally { setLoading(false) }
  }

  async function toggleUser(id: number, active: boolean) {
    try {
      await fetch(`${API}/admin/users/${id}/toggle`, { method: 'PATCH', headers: authHeaders() })
    } catch {}
    setUsers(u => u.map(x => x.id === id ? { ...x, is_active: !active } : x))
  }

  const filtered = users.filter(u =>
    u.username.toLowerCase().includes(search.toLowerCase()) ||
    u.email.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-8">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#FEF0F5' }}>
            <Shield size={20} style={{ color: '#CF6679' }} />
          </div>
          <div>
            <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Admin Panel</h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Platform management & analytics</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 rounded-lg mb-6 w-fit" style={{ background: 'var(--bg-muted)' }}>
          {[
            { key: 'analytics', label: '📊 Analytics' },
            { key: 'users',     label: '👥 Users' },
          ].map(({ key, label }) => (
            <button key={key} onClick={() => setTab(key as typeof tab)}
              className={cn('px-4 py-2 rounded-md text-sm font-medium transition-all', tab === key ? 'shadow-sm' : '')}
              style={{ background: tab === key ? 'var(--bg-card)' : 'transparent', color: tab === key ? 'var(--text-primary)' : 'var(--text-muted)' }}>
              {label}
            </button>
          ))}
        </div>

        {/* ── ANALYTICS ── */}
        {tab === 'analytics' && analytics && (
          <div className="space-y-5">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: 'Total Users',     value: analytics.total_users,      icon: Users,          color: '#1A2744' },
                { label: 'Total Messages',  value: analytics.total_messages,   icon: MessageSquare,  color: '#7A5C1E' },
                { label: 'Docs Analyzed',   value: analytics.total_documents,  icon: FileSearch,     color: '#1A5C35' },
                { label: 'Active Today',    value: analytics.active_today,     icon: TrendingUp,     color: '#CF6679' },
              ].map(({ label, value, icon: Icon, color }) => (
                <div key={label} className="card p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Icon size={14} style={{ color }} />
                    <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{label}</span>
                  </div>
                  <p className="font-display text-3xl font-semibold" style={{ color: 'var(--text-primary)' }}>{value}</p>
                </div>
              ))}
            </div>

            <div className="card p-5">
              <p className="text-sm font-medium mb-4" style={{ color: 'var(--text-primary)' }}>Users by Role</p>
              <div className="space-y-3">
                {Object.entries(analytics.users_by_role).map(([role, count]) => {
                  const info  = ROLES[role as UserRole]
                  const pct   = analytics.total_users > 0 ? (count / analytics.total_users) * 100 : 0
                  return (
                    <div key={role}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs flex items-center gap-1.5" style={{ color: 'var(--text-secondary)' }}>
                          {info?.icon} {info?.label || role}
                        </span>
                        <span className="text-xs font-medium" style={{ color: 'var(--text-primary)' }}>{count}</span>
                      </div>
                      <div className="h-1.5 rounded-full overflow-hidden" style={{ background: 'var(--bg-muted)' }}>
                        <div className="h-full rounded-full transition-all duration-500"
                          style={{ width: `${pct}%`, background: info?.color || 'var(--gold)' }} />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {/* ── USERS ── */}
        {tab === 'users' && (
          <div className="space-y-4">
            <div className="relative">
              <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: 'var(--text-muted)' }} />
              <input className="search-input pl-9" placeholder="Search users by name or email…"
                value={search} onChange={e => setSearch(e.target.value)} />
            </div>

            <div className="card overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr style={{ borderBottom: '0.5px solid var(--border-default)', background: 'var(--bg-muted)' }}>
                    {['User', 'Email', 'Role', 'Joined', 'Status'].map(h => (
                      <th key={h} className="text-left px-4 py-2.5 text-xs font-medium" style={{ color: 'var(--text-muted)' }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {filtered.map(u => {
                    const info = ROLES[u.role]
                    return (
                      <tr key={u.id} className="border-b last:border-0 hover:bg-[var(--bg-muted)] transition-colors"
                        style={{ borderColor: 'var(--border-default)' }}>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium"
                              style={{ background: `${info?.color}20`, color: info?.color }}>
                              {u.username.charAt(0).toUpperCase()}
                            </div>
                            <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{u.username}</span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-xs" style={{ color: 'var(--text-secondary)' }}>{u.email}</td>
                        <td className="px-4 py-3">
                          <span className={cn('mode-badge', `mode-${u.role}`)}>{info?.icon} {info?.label}</span>
                        </td>
                        <td className="px-4 py-3 text-xs" style={{ color: 'var(--text-muted)' }}>
                          {new Date(u.created_at).toLocaleDateString()}
                        </td>
                        <td className="px-4 py-3">
                          <button onClick={() => toggleUser(u.id, u.is_active)}
                            className="text-xs px-2.5 py-1 rounded-full transition-colors"
                            style={{
                              background: u.is_active ? '#F0FBF5' : '#FEF0F0',
                              color:      u.is_active ? '#1A7F4B' : '#C0392B',
                            }}>
                            {u.is_active ? '● Active' : '○ Inactive'}
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
              {filtered.length === 0 && (
                <p className="text-center text-sm py-8" style={{ color: 'var(--text-muted)' }}>No users found</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
