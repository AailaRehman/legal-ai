import Link from 'next/link'
import { Scale } from 'lucide-react'

export function Footer() {
  return (
    <footer
      className="border-t mt-auto"
      style={{ borderColor: 'var(--border-default)' }}
    >
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <div
                className="w-6 h-6 rounded flex items-center justify-center"
                style={{ background: 'var(--navy)' }}
              >
                <Scale size={12} color="#C9A84C" />
              </div>
              <span
                className="font-display font-semibold"
                style={{ color: 'var(--text-primary)' }}
              >
                Mizan
              </span>
            </div>
            <p className="text-xs max-w-xs leading-relaxed" style={{ color: 'var(--text-muted)' }}>
              Pakistan Legal AI Intelligence System. Provides legal information, not legal advice.
              Consult a qualified lawyer for formal matters.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            <div className="flex gap-4">
              {[
                { href: '/chat',     label: 'Legal Chat' },
                { href: '/analyze',  label: 'Analyze' },
                { href: '/draft',    label: 'Draft' },
                { href: '/research', label: 'Research' },
              ].map(({ href, label }) => (
                <Link
                  key={href}
                  href={href}
                  className="text-xs hover:underline"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  {label}
                </Link>
              ))}
            </div>
            <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
              © 2025 Mizan · Built for Pakistan
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
