export type UserRole = 'citizen' | 'lawyer' | 'student' | 'admin'

export interface User {
  id: number
  username: string
  email: string
  role: UserRole
  created_at: string
  last_login?: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface SignupResponse {
  success: boolean
  message: string
}

export const ROLES: Record<UserRole, { label: string; icon: string; color: string; modeDefault: string }> = {
  citizen: { label: 'Citizen',  icon: '🏠', color: '#4CAF7D', modeDefault: 'citizen' },
  lawyer:  { label: 'Lawyer',   icon: '⚖️', color: '#C9A84C', modeDefault: 'lawyer'  },
  student: { label: 'Student',  icon: '📚', color: '#7A8ACF', modeDefault: 'student' },
  admin:   { label: 'Admin',    icon: '🛡️', color: '#CF6679', modeDefault: 'lawyer'  },
}

// Demo accounts (same as Streamlit)
export const DEMO_ACCOUNTS = [
  { username: 'admin',    password: 'admin123',  role: 'admin'   as UserRole },
  { username: 'lawyer1',  password: 'law12345',  role: 'lawyer'  as UserRole },
  { username: 'student1', password: 'stu12345',  role: 'student' as UserRole },
  { username: 'citizen1', password: 'cit12345',  role: 'citizen' as UserRole },
]
