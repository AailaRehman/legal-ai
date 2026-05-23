const STATS = [
  { value: '25+',  label: 'Pakistani law documents' },
  { value: '8',    label: 'Document templates' },
  { value: '3',    label: 'User modes' },
  { value: 'Urdu', label: '+ English support' },
  { value: 'RAG',  label: 'Grounded answers' },
]

export function StatsBar() {
  return (
    <section
      className="border-y py-8"
      style={{ borderColor: 'var(--border-default)' }}
    >
      <div className="max-w-4xl mx-auto px-4">
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-6 text-center">
          {STATS.map(({ value, label }) => (
            <div key={label}>
              <div
                className="font-display text-2xl font-semibold mb-0.5"
                style={{ color: 'var(--gold)' }}
              >
                {value}
              </div>
              <div className="text-xs leading-tight" style={{ color: 'var(--text-muted)' }}>
                {label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
