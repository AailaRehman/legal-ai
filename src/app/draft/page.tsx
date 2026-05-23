import { Navbar } from '@/components/layout/Navbar'
import { Pen } from 'lucide-react'

export default function DraftPage() {
  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <div className="w-14 h-14 rounded-xl flex items-center justify-center mx-auto mb-6"
          style={{ background: '#F0FBF5', border: '0.5px solid #A8D9BB' }}>
          <Pen size={24} style={{ color: '#1A5C35' }} />
        </div>
        <h1 className="font-display text-3xl font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
          Legal Drafter
        </h1>
        <p className="text-sm mb-8" style={{ color: 'var(--text-secondary)' }}>
          Generate affidavits, legal notices, NDAs, FIR drafts, rent agreements, power of attorney and more from smart templates.
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          {['Legal Notice','Affidavit','Rent Agreement','FIR Draft','NDA Agreement','Power of Attorney','Petition','Contract'].map(t => (
            <div key={t} className="card p-3 text-xs text-center" style={{ color: 'var(--text-secondary)' }}>
              {t}
            </div>
          ))}
        </div>
        <div
          className="card p-8 text-sm"
          style={{ color: 'var(--text-muted)', border: '1px dashed var(--border-strong)' }}
        >
          🚧 Coming next — connect FastAPI backend first
        </div>
      </div>
    </div>
  )
}
