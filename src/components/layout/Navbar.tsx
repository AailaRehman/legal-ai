'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Scale, Menu, X } from 'lucide-react'
import { useState } from 'react'
import { ThemeToggle } from '@/components/ui/ThemeToggle'
import { cn } from '@/lib/utils'

const NAV_LINKS = [
  { href: '/chat',     label: 'Legal Chat' },
  { href: '/research', label: 'Research' },
  { href: '/analyze',  label: 'Analyze' },
  { href: '/draft',    label: 'Draft' },
]

export function Navbar() {
  const pathname = usePathname()
  const [open, setOpen] = useState(false)

  return (
    <nav
      className="sticky top-0 z-50 border-b"
      style={{
        background: 'var(--bg-card)',
        borderColor: 'var(--border-default)',
      }}
    >
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 shrink-0">
          <div
            className="w-7 h-7 rounded-md flex items-center justify-center"
            style={{ background: 'var(--navy)' }}
          >
            <Scale size={14} color="#C9A84C" strokeWidth={2} />
          </div>
          <span
            className="font-display text-lg font-semibold tracking-tight"
            style={{ color: 'var(--text-primary)' }}
          >
            Mizan
          </span>
          <span
            className="hidden sm:block text-xs px-1.5 py-0.5 rounded font-mono"
            style={{
              background: 'var(--gold-light)',
              color: 'var(--warning)',
              border: '0.5px solid var(--gold-border)',
            }}
          >
            BETA
          </span>
        </Link>

        {/* Desktop links */}
        <div className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm transition-colors',
                pathname === href
                  ? 'font-medium'
                  : 'hover:bg-[var(--bg-muted)]'
              )}
              style={{
                color: pathname === href ? 'var(--gold)' : 'var(--text-secondary)',
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
          <Link
            href="/dashboard"
            className="hidden md:block btn-ghost text-sm px-3 py-1.5"
          >
            Dashboard
          </Link>
          <Link
            href="/chat"
            className="hidden md:block btn-primary text-sm px-3 py-1.5"
          >
            Ask Mizan
          </Link>
          {/* Mobile menu toggle */}
          <button
            className="md:hidden w-8 h-8 flex items-center justify-center rounded-lg"
            style={{ color: 'var(--text-secondary)' }}
            onClick={() => setOpen(!open)}
            aria-label="Toggle menu"
          >
            {open ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div
          className="md:hidden border-t px-4 py-3 flex flex-col gap-1"
          style={{ borderColor: 'var(--border-default)', background: 'var(--bg-card)' }}
        >
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              onClick={() => setOpen(false)}
              className={cn(
                'px-3 py-2 rounded-lg text-sm',
                pathname === href ? 'font-medium' : ''
              )}
              style={{ color: pathname === href ? 'var(--gold)' : 'var(--text-secondary)' }}
            >
              {label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
