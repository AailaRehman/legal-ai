'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Scale, Eye, EyeOff, AlertCircle, ChevronRight } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'
import { ThemeToggle } from '@/components/ui/ThemeToggle'
import type { UserRole } from '@/lib/auth.types'
import { ROLES, DEMO_ACCOUNTS } from '@/lib/auth.types'
import { cn } from '@/lib/utils'

type Tab = 'login' | 'signup'

export default function LoginPage() {
  const { login, signup, isLoading } = useAuth()
  const router = useRouter()

  const [tab, setTab]           = useState<Tab>('login')
  const [error, setError]       = useState('')
  const [success, setSuccess]   = useState('')
  const [showPass, setShowPass] = useState(false)

  // Login fields
  const [loginForm, setLoginForm] = useState({ username: '', password: '' })

  // Signup fields
  const [signupForm, setSignupForm] = useState({
    username: '', email: '', password: '', confirm: '', role: 'citizen' as UserRole,
  })

  // ── Login submit ──────────────────────────────────────────────
  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (!loginForm.username || !loginForm.password) {
      setError('Please enter your username and password.')
      return
    }
    try {
      await login(loginForm.username, loginForm.password)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Login failed')
    }
  }

  // ── Signup submit ─────────────────────────────────────────────
  async function handleSignup(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setSuccess('')
    const { username, email, password, confirm, role } = signupForm
    if (!username || !email || !password || !confirm) {
      setError('All fields are required.')
      return
    }
    if (username.length < 3) { setError('Username must be at least 3 characters.'); return }
    if (password.length < 6) { setError('Password must be at least 6 characters.'); return }
    if (password !== confirm) { setError('Passwords do not match.'); return }
    if (!email.includes('@'))  { setError('Invalid email address.'); return }

    try {
      const res = await signup(username, email, password, role)
      if (res.success) {
        setSuccess('Account created! You can now log in.')
        setTab('login')
        setLoginForm({ username, password: '' })
      } else {
        setError(res.message)
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Signup failed')
    }
  }

  // ── Demo login ────────────────────────────────────────────────
  async function demoLogin(username: string, password: string) {
    setError('')
    setTab('login')
    setLoginForm({ username, password })
    try {
      await login(username, password)
    } catch {
      // Backend not connected — still fill form visually
      setError('Backend not connected yet. Fill in credentials manually once FastAPI is running.')
    }
  }

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ background: 'var(--bg-page)' }}
    >
      {/* Top bar */}
      <div
        className="flex items-center justify-between px-6 py-4 border-b"
        style={{ borderColor: 'var(--border-default)', background: 'var(--bg-card)' }}
      >
        <button
          onClick={() => router.push('/')}
          className="flex items-center gap-2"
        >
          <div className="w-7 h-7 rounded-md flex items-center justify-center" style={{ background: 'var(--navy)' }}>
            <Scale size={14} color="#C9A84C" />
          </div>
          <span className="font-display font-semibold" style={{ color: 'var(--text-primary)' }}>Mizan</span>
        </button>
        <ThemeToggle />
      </div>

      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">

          {/* Card */}
          <div className="card-elevated p-8">
            <div className="text-center mb-7">
              <h1 className="font-display text-2xl font-semibold mb-1" style={{ color: 'var(--text-primary)' }}>
                {tab === 'login' ? 'Welcome back' : 'Create account'}
              </h1>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                {tab === 'login'
                  ? 'Sign in to access Mizan Legal AI'
                  : 'Join Mizan to save your legal history'}
              </p>
            </div>

            {/* Tabs */}
            <div
              className="flex rounded-lg p-1 mb-6"
              style={{ background: 'var(--bg-muted)' }}
            >
              {(['login', 'signup'] as Tab[]).map(t => (
                <button
                  key={t}
                  onClick={() => { setTab(t); setError(''); setSuccess('') }}
                  className={cn(
                    'flex-1 py-2 rounded-md text-sm font-medium transition-all',
                    tab === t ? 'shadow-sm' : ''
                  )}
                  style={{
                    background: tab === t ? 'var(--bg-card)' : 'transparent',
                    color:      tab === t ? 'var(--text-primary)' : 'var(--text-muted)',
                  }}
                >
                  {t === 'login' ? 'Sign in' : 'Sign up'}
                </button>
              ))}
            </div>

            {/* Error / success banners */}
            {error && (
              <div
                className="flex items-start gap-2 px-3 py-2.5 rounded-lg mb-4 text-sm"
                style={{ background: '#FEF0F0', color: '#C0392B', border: '0.5px solid #F5C6C6' }}
              >
                <AlertCircle size={15} className="shrink-0 mt-0.5" />
                {error}
              </div>
            )}
            {success && (
              <div
                className="flex items-center gap-2 px-3 py-2.5 rounded-lg mb-4 text-sm"
                style={{ background: '#F0FBF5', color: '#1A7F4B', border: '0.5px solid #A8D9BB' }}
              >
                ✓ {success}
              </div>
            )}

            {/* ── LOGIN FORM ── */}
            {tab === 'login' && (
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                    Username
                  </label>
                  <input
                    className="search-input"
                    placeholder="Enter your username"
                    value={loginForm.username}
                    onChange={e => setLoginForm(f => ({ ...f, username: e.target.value }))}
                    autoComplete="username"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                    Password
                  </label>
                  <div className="relative">
                    <input
                      type={showPass ? 'text' : 'password'}
                      className="search-input pr-10"
                      placeholder="Enter your password"
                      value={loginForm.password}
                      onChange={e => setLoginForm(f => ({ ...f, password: e.target.value }))}
                      autoComplete="current-password"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPass(!showPass)}
                      className="absolute right-3 top-1/2 -translate-y-1/2"
                      style={{ color: 'var(--text-muted)' }}
                    >
                      {showPass ? <EyeOff size={15} /> : <Eye size={15} />}
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="btn-primary w-full py-2.5 text-sm flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {isLoading ? 'Signing in…' : <>Sign in <ChevronRight size={14} /></>}
                </button>
              </form>
            )}

            {/* ── SIGNUP FORM ── */}
            {tab === 'signup' && (
              <form onSubmit={handleSignup} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                      Username
                    </label>
                    <input
                      className="search-input"
                      placeholder="min. 3 chars"
                      value={signupForm.username}
                      onChange={e => setSignupForm(f => ({ ...f, username: e.target.value }))}
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                      Email
                    </label>
                    <input
                      type="email"
                      className="search-input"
                      placeholder="you@email.com"
                      value={signupForm.email}
                      onChange={e => setSignupForm(f => ({ ...f, email: e.target.value }))}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                    I am a…
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {(Object.entries(ROLES) as [UserRole, typeof ROLES[UserRole]][])
                      .filter(([r]) => r !== 'admin')
                      .map(([role, info]) => (
                        <button
                          key={role}
                          type="button"
                          onClick={() => setSignupForm(f => ({ ...f, role }))}
                          className={cn(
                            'flex items-center gap-2 px-3 py-2 rounded-lg text-left text-sm transition-all',
                            signupForm.role === role ? 'ring-1' : ''
                          )}
                          style={{
                            background:   signupForm.role === role ? `${info.color}18` : 'var(--bg-muted)',
                            color:        signupForm.role === role ? info.color : 'var(--text-secondary)',
                            borderColor:  signupForm.role === role ? info.color : 'transparent',
                            border:       signupForm.role === role ? `0.5px solid ${info.color}` : '0.5px solid var(--border-default)',
                          }}
                        >
                          <span>{info.icon}</span>
                          <span className="font-medium">{info.label}</span>
                        </button>
                      ))
                    }
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                      Password
                    </label>
                    <input
                      type="password"
                      className="search-input"
                      placeholder="min. 6 chars"
                      value={signupForm.password}
                      onChange={e => setSignupForm(f => ({ ...f, password: e.target.value }))}
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                      Confirm
                    </label>
                    <input
                      type="password"
                      className="search-input"
                      placeholder="repeat password"
                      value={signupForm.confirm}
                      onChange={e => setSignupForm(f => ({ ...f, confirm: e.target.value }))}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="btn-primary w-full py-2.5 text-sm flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {isLoading ? 'Creating account…' : <>Create account <ChevronRight size={14} /></>}
                </button>
              </form>
            )}
          </div>

          {/* Demo accounts */}
          <div className="mt-5">
            <p className="text-xs text-center mb-3" style={{ color: 'var(--text-muted)' }}>
              — Demo accounts (no backend needed once FastAPI is running) —
            </p>
            <div className="grid grid-cols-2 gap-2">
              {DEMO_ACCOUNTS.map(({ username, password, role }) => {
                const info = ROLES[role]
                return (
                  <button
                    key={username}
                    onClick={() => demoLogin(username, password)}
                    className="card flex items-center gap-2.5 px-3 py-2.5 text-left hover:shadow-sm transition-all"
                  >
                    <span className="text-base">{info.icon}</span>
                    <div>
                      <p className="text-xs font-medium" style={{ color: 'var(--text-primary)' }}>
                        {username}
                      </p>
                      <p className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
                        {password} · {info.label}
                      </p>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
