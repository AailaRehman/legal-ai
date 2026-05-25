'use client'

import {
  createContext, useContext, useEffect, useState, useCallback,
  type ReactNode,
} from 'react'
import { useRouter } from 'next/navigation'
import type { User, UserRole } from '@/lib/auth.types'
import { ROLES } from '@/lib/auth.types'
import {
  apiLogin, apiSignup, getToken, setToken, removeToken,
  getStoredUser, setStoredUser,
} from '@/lib/auth.api'

interface AuthContextType {
  user:            User | null
  isAuthenticated: boolean
  isLoading:       boolean
  login:           (username: string, password: string) => Promise<void>
  signup:          (username: string, email: string, password: string, role: UserRole) => Promise<{ success: boolean; message: string }>
  logout:          () => void
  isAdmin:         () => boolean
  roleInfo:        () => typeof ROLES[UserRole]
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const router  = useRouter()
  const [user, setUser]         = useState<User | null>(null)
  const [isLoading, setLoading] = useState(true)

  // Rehydrate from localStorage on mount
  useEffect(() => {
    const token       = getToken()
    const storedUser  = getStoredUser()
    if (token && storedUser) {
      setUser(storedUser)
    }
    setLoading(false)
  }, [])

  const login = useCallback(async (username: string, password: string) => {
    setLoading(true)
    try {
      const data = await apiLogin(username, password)
      setToken(data.access_token)
      setStoredUser(data.user)
      setUser(data.user)
      // Redirect based on role
      router.push('/chat')
    } finally {
      setLoading(false)
    }
  }, [router])

  const signup = useCallback(async (
    username: string,
    email: string,
    password: string,
    role: UserRole
  ) => {
    const result = await apiSignup(username, email, password, role)
    return result
  }, [])

  const logout = useCallback(() => {
    removeToken()
    setUser(null)
    router.push('/login')
  }, [router])

  const isAdmin   = useCallback(() => user?.role === 'admin', [user])
  const roleInfo  = useCallback(() => ROLES[user?.role ?? 'citizen'], [user])

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      signup,
      logout,
      isAdmin,
      roleInfo,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
