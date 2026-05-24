'use client'

import { useHealth } from '@/hooks/useHealth'
import { AlertTriangle, CheckCircle, Loader2, Database } from 'lucide-react'

export function BackendStatus() {
  const health = useHealth()

  if (health.loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs"
        style={{ background: 'var(--bg-muted)', color: 'var(--text-muted)' }}>
        <Loader2 size={11} className="animate-spin" />
        Connecting to backend…
      </div>
    )
  }

  if (health.status === 'offline') {
    return (
      <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg text-xs"
        style={{ background: '#FEF0F0', color: '#C0392B', border: '0.5px solid #F5C6C6' }}>
        <AlertTriangle size={11} className="shrink-0 mt-0.5" />
        <div>
          <p className="font-medium">Backend offline</p>
          <p className="opacity-80">Start FastAPI: <code className="font-mono">uvicorn main:app</code></p>
        </div>
      </div>
    )
  }

  if (!health.kb_ready) {
    return (
      <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg text-xs"
        style={{ background: '#FEF9ED', color: '#7A5C1E', border: '0.5px solid var(--gold-border)' }}>
        <Database size={11} className="shrink-0 mt-0.5" />
        <div>
          <p className="font-medium">Knowledge base not built</p>
          <p className="opacity-80">Run: <code className="font-mono">python scripts/build_kb.py</code></p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs"
      style={{ background: '#F0FBF5', color: '#1A7F4B', border: '0.5px solid #A8D9BB' }}>
      <CheckCircle size={11} />
      Backend connected · KB ready
    </div>
  )
}
