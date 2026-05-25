'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import type { UserRole } from '@/lib/auth.types'

interface Props {
  children: React.ReactNode
  requiredRole?: UserRole   // if set, only that role can access
}

export function RequireAuth({ children, requiredRole }: Props) {
  const { isAuthenticated, isLoading, user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (isLoading) return
    if (!isAuthenticated) {
      router.replace('/login')
      return
    }
    if (requiredRole && user?.role !== requiredRole && user?.role !== 'admin') {
      router.replace('/chat')
    }
  }, [isAuthenticated, isLoading, user, requiredRole, router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: 'var(--bg-page)' }}>
        <div className="flex flex-col items-center gap-3">
          <div className="flex gap-1.5">
            <div className="typing-dot" />
            <div className="typing-dot" />
            <div className="typing-dot" />
          </div>
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>Loading…</span>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) return null
  if (requiredRole && user?.role !== requiredRole && user?.role !== 'admin') return null

  return <>{children}</>
}
