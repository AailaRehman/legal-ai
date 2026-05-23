import type { LoginResponse, SignupResponse, User, UserRole } from './auth.types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// ── Token storage ─────────────────────────────────────────────
export function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('mizan_token')
}

export function setToken(token: string) {
  localStorage.setItem('mizan_token', token)
}

export function removeToken() {
  localStorage.removeItem('mizan_token')
  localStorage.removeItem('mizan_user')
}

export function getStoredUser(): User | null {
  if (typeof window === 'undefined') return null
  try {
    const raw = localStorage.getItem('mizan_user')
    return raw ? JSON.parse(raw) : null
  } catch { return null }
}

export function setStoredUser(user: User) {
  localStorage.setItem('mizan_user', JSON.stringify(user))
}

// ── Auth headers ──────────────────────────────────────────────
export function authHeaders(): Record<string, string> {
  const token = getToken()
  return token
    ? { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
    : { 'Content-Type': 'application/json' }
}

// ── Login ─────────────────────────────────────────────────────
export async function apiLogin(
  username: string,
  password: string
): Promise<LoginResponse> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ username, password }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Invalid username or password')
  }
  return res.json()
}

// ── Signup ────────────────────────────────────────────────────
export async function apiSignup(
  username: string,
  email: string,
  password: string,
  role: UserRole = 'citizen'
): Promise<SignupResponse> {
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ username, email, password, role }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Signup failed')
  }
  return res.json()
}

// ── Get current user ──────────────────────────────────────────
export async function apiGetMe(): Promise<User> {
  const res = await fetch(`${API_BASE}/auth/me`, { headers: authHeaders() })
  if (!res.ok) throw new Error('Unauthorized')
  return res.json()
}
