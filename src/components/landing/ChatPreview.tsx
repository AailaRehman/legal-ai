import { Scale } from 'lucide-react'

const DEMO_EXCHANGE = {
  question: 'Can my landlord evict me without a court order in Pakistan?',
  answer: `No. Under Pakistani law, a landlord cannot forcibly evict a tenant without first obtaining a court order from the Rent Tribunal.

The landlord must file an eviction application citing a valid ground — such as personal need, non-payment, or misuse of premises. The tenant has the right to contest. Forcible eviction without a court order may constitute criminal trespass and breach of the Rent Restriction Ordinance.`,
  sources: [
    { law: 'Rent Restriction Ordinance', section: '1959, §17' },
    { law: 'Pakistan Penal Code',         section: 'Section 441' },
    { law: 'CrPC',                        section: 'Section 145' },
  ],
}

export function ChatPreview() {
  return (
    <section className="max-w-4xl mx-auto px-4 pb-16">
      <div className="text-center mb-8">
        <h2
          className="font-display text-3xl font-semibold mb-2"
          style={{ color: 'var(--text-primary)' }}
        >
          See it in action
        </h2>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Every answer is grounded in Pakistani law with precise citations.
        </p>
      </div>

      <div
        className="card-elevated overflow-hidden"
        style={{ border: '0.5px solid var(--border-default)' }}
      >
        {/* Window chrome */}
        <div
          className="flex items-center gap-2 px-4 py-3 border-b"
          style={{ borderColor: 'var(--border-default)', background: 'var(--bg-muted)' }}
        >
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full" style={{ background: '#FF5F57' }} />
            <div className="w-3 h-3 rounded-full" style={{ background: '#FEBC2E' }} />
            <div className="w-3 h-3 rounded-full" style={{ background: '#28C840' }} />
          </div>
          <span className="text-xs ml-2" style={{ color: 'var(--text-muted)' }}>
            Mizan Legal Chat · Citizen mode
          </span>
        </div>

        <div className="p-6 space-y-5">
          {/* User message */}
          <div className="flex justify-end">
            <div
              className="max-w-sm px-4 py-3 rounded-2xl rounded-tr-sm text-sm leading-relaxed"
              style={{
                background: 'var(--chat-user-bg)',
                color: 'var(--chat-user-fg)',
              }}
            >
              {DEMO_EXCHANGE.question}
            </div>
          </div>

          {/* AI message */}
          <div className="flex gap-3 items-start">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
              style={{ background: 'var(--navy)' }}
            >
              <Scale size={14} color="#C9A84C" />
            </div>
            <div className="flex-1">
              <div
                className="px-4 py-3 rounded-2xl rounded-tl-sm text-sm leading-relaxed whitespace-pre-line"
                style={{
                  background: 'var(--chat-ai-bg)',
                  color: 'var(--chat-ai-fg)',
                }}
              >
                {DEMO_EXCHANGE.answer}
              </div>

              {/* Citations */}
              <div className="mt-3 flex flex-wrap gap-1.5">
                <span className="text-xs mr-1" style={{ color: 'var(--text-muted)' }}>Sources:</span>
                {DEMO_EXCHANGE.sources.map(s => (
                  <span key={s.section} className="citation-chip">
                    {s.law} · {s.section}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
