import { Navbar } from '@/components/layout/Navbar'
import { BookOpen } from 'lucide-react'

const LAWS = [
  { name: 'Constitution of Pakistan', year: '1973', sections: '280+' },
  { name: 'Pakistan Penal Code',      year: '1860', sections: '511' },
  { name: 'Code of Criminal Procedure', year: '1898', sections: '565' },
  { name: 'PECA 2016',               year: '2016', sections: '48' },
  { name: 'Muslim Family Laws Ordinance', year: '1961', sections: '12' },
  { name: 'Contract Act',            year: '1872', sections: '238' },
  { name: 'Transfer of Property Act', year: '1882', sections: '137' },
  { name: 'Income Tax Ordinance',    year: '2001', sections: '240+' },
]

export default function ResearchPage() {
  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center"
            style={{ background: '#FEF0F0' }}>
            <BookOpen size={20} style={{ color: '#5C1A1A' }} />
          </div>
          <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
            Law Research
          </h1>
        </div>
        <p className="text-sm mb-8 ml-13" style={{ color: 'var(--text-secondary)' }}>
          Browse 25+ Pakistani law documents. Semantic search coming with backend.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {LAWS.map(law => (
            <div key={law.name} className="card p-4 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{law.name}</p>
                <p className="text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>{law.year} · {law.sections} sections</p>
              </div>
              <span className="citation-chip">PDF</span>
            </div>
          ))}
        </div>

        <div className="card p-6 mt-6 text-center text-sm" style={{ color: 'var(--text-muted)', border: '1px dashed var(--border-strong)' }}>
          🚧 Semantic search across sections — coming with FastAPI + FAISS backend
        </div>
      </div>
    </div>
  )
}
