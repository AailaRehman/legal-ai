import { Navbar } from '@/components/layout/Navbar'
import { LayoutDashboard } from 'lucide-react'

export default function DashboardPage() {
  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center"
            style={{ background: 'var(--navy-light)' }}>
            <LayoutDashboard size={20} style={{ color: 'var(--navy)' }} />
          </div>
          <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
            Dashboard
          </h1>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Conversations', value: '0' },
            { label: 'Documents Analyzed', value: '0' },
            { label: 'Drafts Generated', value: '0' },
            { label: 'Saved Items', value: '0' },
          ].map(s => (
            <div key={s.label} className="card p-4 text-center">
              <p className="font-display text-3xl font-semibold" style={{ color: 'var(--gold)' }}>{s.value}</p>
              <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>{s.label}</p>
            </div>
          ))}
        </div>

        <div className="card p-8 text-center text-sm" style={{ color: 'var(--text-muted)', border: '1px dashed var(--border-strong)' }}>
          🚧 Auth + saved history — coming after FastAPI backend
        </div>
      </div>
    </div>
  )
}
