import Link from 'next/link'
import { MessageSquare, FileSearch, Pen, BookOpen, Scale, GraduationCap } from 'lucide-react'

const FEATURES = [
  {
    icon:     MessageSquare,
    title:    'Legal Chat',
    desc:     'Ask any legal question in English or Urdu. Get cited answers from PPC, CrPC, Constitution and more.',
    href:     '/chat',
    color:    'var(--navy)',
    bgColor:  '#EEF1F8',
    darkBg:   'rgba(58, 84, 153, 0.15)',
    badge:    'Core feature',
  },
  {
    icon:     FileSearch,
    title:    'Document Analyzer',
    desc:     'Upload contracts, FIRs, rent agreements. Get risk scores, missing clauses, and plain-language summaries.',
    href:     '/analyze',
    color:    '#7A5C1E',
    bgColor:  '#FEF9ED',
    darkBg:   'rgba(201, 168, 76, 0.12)',
    badge:    null,
  },
  {
    icon:     Pen,
    title:    'Legal Drafter',
    desc:     'Generate affidavits, legal notices, NDAs, FIR drafts, rent agreements and more from smart templates.',
    href:     '/draft',
    color:    '#1A5C35',
    bgColor:  '#F0FBF5',
    darkBg:   'rgba(29, 110, 63, 0.15)',
    badge:    null,
  },
  {
    icon:     BookOpen,
    title:    'Law Research',
    desc:     'Search across 25+ Pakistani law documents. Browse by act, section, or topic with semantic search.',
    href:     '/research',
    color:    '#5C1A1A',
    bgColor:  '#FEF0F0',
    darkBg:   'rgba(192, 57, 43, 0.12)',
    badge:    null,
  },
  {
    icon:     Scale,
    title:    'Case Strategy',
    desc:     'Describe your situation and get structured legal strategy, court procedures, and next steps.',
    href:     '/chat?mode=lawyer',
    color:    '#1A3A5C',
    bgColor:  '#EEF4FB',
    darkBg:   'rgba(24, 95, 165, 0.12)',
    badge:    'Lawyer mode',
  },
  {
    icon:     GraduationCap,
    title:    'Legal Education',
    desc:     'MCQs, case scenarios, and plain-language explanations of Pakistani law — perfect for law students.',
    href:     '/chat?mode=student',
    color:    '#3A1A5C',
    bgColor:  '#F4EEF8',
    darkBg:   'rgba(83, 74, 183, 0.12)',
    badge:    'Student mode',
  },
]

export function Features() {
  return (
    <section className="max-w-6xl mx-auto px-4 py-16">
      <div className="text-center mb-12">
        <h2
          className="font-display text-3xl font-semibold mb-3"
          style={{ color: 'var(--text-primary)' }}
        >
          Everything you need
        </h2>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Six tools, one platform, all grounded in Pakistani law.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {FEATURES.map(({ icon: Icon, title, desc, href, color, bgColor, darkBg, badge }) => (
          <Link
            key={href}
            href={href}
            className="card p-5 flex flex-col gap-3 group transition-all hover:shadow-sm hover:-translate-y-0.5 duration-200"
          >
            <div className="flex items-start justify-between">
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ background: bgColor }}
              >
                <Icon size={18} style={{ color }} />
              </div>
              {badge && (
                <span
                  className="text-xs px-2 py-0.5 rounded-full font-medium"
                  style={{
                    background: bgColor,
                    color,
                    border: `0.5px solid ${color}30`,
                  }}
                >
                  {badge}
                </span>
              )}
            </div>

            <div>
              <h3
                className="font-display text-base font-semibold mb-1 group-hover:text-[var(--gold)] transition-colors"
                style={{ color: 'var(--text-primary)' }}
              >
                {title}
              </h3>
              <p className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                {desc}
              </p>
            </div>

            <div
              className="text-xs font-medium flex items-center gap-1 mt-auto"
              style={{ color: 'var(--gold)' }}
            >
              Open →
            </div>
          </Link>
        ))}
      </div>
    </section>
  )
}
