import { Navbar } from '@/components/layout/Navbar'
import { FileSearch } from 'lucide-react'

export default function AnalyzePage() {
  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <div className="w-14 h-14 rounded-xl flex items-center justify-center mx-auto mb-6"
          style={{ background: 'var(--gold-light)', border: '0.5px solid var(--gold-border)' }}>
          <FileSearch size={24} style={{ color: 'var(--warning)' }} />
        </div>
        <h1 className="font-display text-3xl font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
          Document Analyzer
        </h1>
        <p className="text-sm mb-8" style={{ color: 'var(--text-secondary)' }}>
          Upload contracts, FIRs, rent agreements and get AI-powered risk analysis, entity extraction, and plain-language summaries.
        </p>
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
