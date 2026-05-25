'use client'

import { useState, useEffect } from 'react'

interface HealthStatus {
  status:   string
  kb_ready: boolean
  loading:  boolean
}

export function useHealth() {
  const [health, setHealth] = useState<HealthStatus>({ status: 'unknown', kb_ready: false, loading: true })

  useEffect(() => {
    async function check() {
      try {
        const res  = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/health')
        const data = await res.json()
        setHealth({ ...data, loading: false })
      } catch {
        setHealth({ status: 'offline', kb_ready: false, loading: false })
      }
    }
    check()
    const interval = setInterval(check, 30000)  // recheck every 30s
    return () => clearInterval(interval)
  }, [])

  return health
}
