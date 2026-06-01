'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Scale, Menu, X, LogOut, LayoutDashboard, Shield } from 'lucide-react'
import { useState } from 'react'
import { ThemeToggle }  from '@/components/ui/ThemeToggle'
import { useAuth }      from '@/contexts/AuthContext'
import { ROLES }        from '@/lib/auth.types'
import { cn }           from '@/lib/utils'

const NAV_LINKS = [
  { href: '/chat',     label: 'Legal Chat' },
  { href: '/analyze',  label: 'Analyze'    },
  { href: '/draft',      label: 'Draft'      },
  { href: '/strategy',  label: 'Strategy'   },
  { href: '/education', label: 'Education'  },
  { href: '/multilingual', label: 'Urdu Chat' },
]

export function Navbar() {
  const pathname                    = usePathname()
  const [menuOpen, setMenuOpen]     = useState(false)
  const [userOpen, setUserOpen]     = useState(false)
  const { user, isAuthenticated, logout, isAdmin } = useAuth()

  const roleInfo = user ? ROLES[user.role] : null

  return (
    <nav
      className="sticky top-0 z-50 border-b"
      style={{ background: 'var(--bg-card)', borderColor: 'var(--border-default)' }}
    >
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">

        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 shrink-0">
          <div className="w-7 h-7 rounded-md flex items-center justify-center" style={{ background: 'var(--navy)' }}>
            <Scale size={14} color="#C9A84C" strokeWidth={2} />
          </div>
          <span className="font-display text-lg font-semibold tracking-tight" style={{ color: 'var(--text-primary)' }}>
            Mizan
          </span>
          <span
            className="hidden sm:block text-xs px-1.5 py-0.5 rounded font-mono"
            style={{ background: 'var(--gold-light)', color: 'var(--warning)', border: '0.5px solid var(--gold-border)' }}
          >
            BETA
          </span>
        </Link>

        {/* Desktop nav links */}
        <div className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={cn('px-3 py-1.5 rounded-lg text-sm transition-colors', pathname === href ? 'font-medium' : 'hover:bg-[var(--bg-muted)]')}
              style={{
                color:      pathname === href ? 'var(--gold)' : 'var(--text-secondary)',
                background: pathname === href ? 'var(--gold-light)' : undefined,
              }}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2">
          <ThemeToggle />

          {isAuthenticated && user ? (
            <div className="relative">
              <button
                onClick={() => setUserOpen(!userOpen)}
                className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg transition-colors hover:bg-[var(--bg-muted)]"
              >
                <div
                  className="w-7 h-7 rounded-full flex items-center justify-center text-sm font-medium"
                  style={{ background: `${roleInfo?.color}22`, color: roleInfo?.color }}
                >
                  {user.username.charAt(0).toUpperCase()}
                </div>
                <span className="hidden sm:block text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                  {user.username}
                </span>
                <span className={cn('hidden sm:block mode-badge', `mode-${user.role}`)}>
                  {roleInfo?.icon} {roleInfo?.label}
                </span>
              </button>

              {userOpen && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setUserOpen(false)} />
                  <div
                    className="absolute right-0 top-full mt-1.5 w-52 rounded-xl shadow-lg z-20 overflow-hidden"
                    style={{ background: 'var(--bg-elevated)', border: '0.5px solid var(--border-default)' }}
                  >
                    <div className="px-4 py-3 border-b" style={{ borderColor: 'var(--border-default)' }}>
                      <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{user.username}</p>
                      <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{user.email}</p>
                    </div>
                    <div className="py-1">
                      <Link
                        href="/dashboard"
                        onClick={() => setUserOpen(false)}
                        className="flex items-center gap-2.5 px-4 py-2.5 text-sm hover:bg-[var(--bg-muted)] transition-colors"
                        style={{ color: 'var(--text-secondary)' }}
                      >
                        <LayoutDashboard size={14} />
                        Dashboard
                      </Link>
                      {isAdmin() && (
                        <Link
                          href="/admin"
                          onClick={() => setUserOpen(false)}
                          className="flex items-center gap-2.5 px-4 py-2.5 text-sm hover:bg-[var(--bg-muted)] transition-colors"
                          style={{ color: '#CF6679' }}
                        >
                          <Shield size={14} />
                          Admin Panel
                        </Link>
                      )}
                      <button
                        onClick={() => { logout(); setUserOpen(false) }}
                        className="w-full flex items-center gap-2.5 px-4 py-2.5 text-sm hover:bg-[var(--bg-muted)] transition-colors"
                        style={{ color: 'var(--text-secondary)' }}
                      >
                        <LogOut size={14} />
                        Sign out
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          ) : (
            <>
              <Link href="/login" className="hidden md:block btn-ghost text-sm px-3 py-1.5">
                Sign in
              </Link>
              <Link href="/login" className="hidden md:block btn-primary text-sm px-3 py-1.5">
                Get started
              </Link>
            </>
          )}

          <button
            className="md:hidden w-8 h-8 flex items-center justify-center rounded-lg"
            style={{ color: 'var(--text-secondary)' }}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <div
          className="md:hidden border-t px-4 py-3 flex flex-col gap-1"
          style={{ borderColor: 'var(--border-default)', background: 'var(--bg-card)' }}
        >
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              onClick={() => setMenuOpen(false)}
              className={cn('px-3 py-2 rounded-lg text-sm', pathname === href ? 'font-medium' : '')}
              style={{ color: pathname === href ? 'var(--gold)' : 'var(--text-secondary)' }}
            >
              {label}
            </Link>
          ))}
          {!isAuthenticated && (
            <Link href="/login" onClick={() => setMenuOpen(false)} className="px-3 py-2 text-sm" style={{ color: 'var(--gold)' }}>
              Sign in / Sign up
            </Link>
          )}
          {isAuthenticated && (
            <button onClick={() => { logout(); setMenuOpen(false) }} className="px-3 py-2 text-sm text-left" style={{ color: 'var(--text-secondary)' }}>
              Sign out
            </button>
          )}
        </div>
      )}
    </nav>
  )
}
