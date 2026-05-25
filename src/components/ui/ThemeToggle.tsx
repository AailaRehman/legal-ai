'use client'

import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'
import { Sun, Moon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ThemeToggleProps {
  className?: string
}

export function ThemeToggle({ className }: ThemeToggleProps) {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => setMounted(true), [])
  if (!mounted) return <div className="w-8 h-8" />

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className={cn(
        'w-8 h-8 rounded-lg flex items-center justify-center',
        'border transition-all duration-150',
        'hover:bg-[var(--bg-muted)]',
        className
      )}
      style={{ borderColor: 'var(--border-default)', color: 'var(--text-secondary)' }}
      aria-label="Toggle theme"
    >
      {theme === 'dark'
        ? <Sun size={15} />
        : <Moon size={15} />
      }
    </button>
  )
}
