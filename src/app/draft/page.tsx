'use client'

import { useState } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { Pen, Loader2, Copy, Check, Download } from 'lucide-react'
import { cn } from '@/lib/utils'

const TEMPLATES: Record<string, { fields: Record<string, string>; icon: string; desc: string }> = {
  'Legal Notice': {
    icon: '📋', desc: 'Formal notice demanding action or payment',
    fields: { sender_name: 'Your Full Name', sender_address: 'Your Address', recipient_name: "Recipient's Name", recipient_address: "Recipient's Address", subject: 'Subject of Notice', facts: 'Facts & Background', demand: 'What You Are Demanding', deadline: 'Response Deadline (days)' },
  },
  'Affidavit': {
    icon: '📜', desc: 'Sworn statement for court or official use',
    fields: { deponent_name: 'Your Full Name', deponent_cnic: 'CNIC Number', deponent_address: 'Your Address', purpose: 'Purpose of Affidavit', facts: 'Facts to Declare (numbered)', city: 'City' },
  },
  'Rent Agreement': {
    icon: '🏠', desc: 'Residential or commercial rent agreement',
    fields: { landlord_name: "Landlord's Full Name", tenant_name: "Tenant's Full Name", property_address: 'Property Address', monthly_rent: 'Monthly Rent (PKR)', security_deposit: 'Security Deposit (PKR)', start_date: 'Start Date', duration: 'Duration (months)', special_terms: 'Special Terms (optional)' },
  },
  'FIR Draft': {
    icon: '🚔', desc: 'FIR complaint under Section 154 CrPC',
    fields: { complainant_name: 'Your Full Name', complainant_cnic: 'Your CNIC', complainant_address: 'Your Address', police_station: 'Police Station Name', accused_name: "Accused Person's Name/Description", incident_date: 'Date of Incident', incident_place: 'Place of Incident', incident_details: 'Detailed Description of Incident', sections_violated: 'Sections of Law Violated (if known)' },
  },
  'NDA Agreement': {
    icon: '🔒', desc: 'Non-Disclosure Agreement',
    fields: { party_a: 'Party A (Disclosing Party)', party_b: 'Party B (Receiving Party)', purpose: 'Purpose of Disclosure', duration: 'Duration of Confidentiality (years)', governing_law: 'Governing Jurisdiction (city)', effective_date: 'Effective Date' },
  },
  'Power of Attorney': {
    icon: '📝', desc: 'Authorise someone to act on your behalf',
    fields: { principal_name: 'Principal (Your Name)', principal_cnic: 'Principal CNIC', attorney_name: "Attorney's Full Name", attorney_cnic: "Attorney's CNIC", powers_granted: 'Specific Powers to Grant', property_details: 'Property/Matter Details (if applicable)', duration: 'Duration (leave blank for general)' },
  },
  'Petition': {
    icon: '⚖️', desc: 'Court petition for relief',
    fields: { petitioner: "Petitioner's Name", respondent: "Respondent's Name", court: 'Court Name', jurisdiction: 'Jurisdiction Basis', facts: 'Statement of Facts', legal_grounds: 'Legal Grounds', relief_sought: 'Relief/Prayer Sought' },
  },
  'Contract Agreement': {
    icon: '🤝', desc: 'General contract under Contract Act 1872',
    fields: { party_a: 'Party A Name', party_b: 'Party B Name', subject_matter: 'Subject Matter of Contract', obligations_a: "Party A's Obligations", obligations_b: "Party B's Obligations", consideration: 'Consideration/Payment Terms', duration: 'Contract Duration', dispute_resolution: 'Dispute Resolution Method' },
  },
}

export default function DraftPage() {
  const [docType, setDocType]   = useState('Legal Notice')
  const [fields, setFields]     = useState<Record<string, string>>({})
  const [result, setResult]     = useState('')
  const [loading, setLoading]   = useState(false)
  const [copied, setCopied]     = useState(false)

  const template = TEMPLATES[docType]

  function setField(key: string, value: string) {
    setFields(f => ({ ...f, [key]: value }))
  }

  async function handleDraft() {
    setResult(''); setLoading(true)
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ doc_type: docType, fields }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setResult(data.content)
    } catch {
      // Demo output
      const filledFields = Object.entries(fields).map(([k, v]) => `${k.replace(/_/g, ' ')}: ${v}`).join('\n')
      setResult(`[Backend not connected — preview structure]\n\n${docType.toUpperCase()}\n${'='.repeat(50)}\n\nProvided details:\n${filledFields || '(no fields filled)'}\n\nOnce FastAPI is running with your GROQ_API_KEY, a complete professionally drafted ${docType} will appear here — ready to print, sign, and use under Pakistani law.\n\nThe document will include:\n• Proper legal heading and date\n• All party details formatted correctly\n• Relevant Pakistani law citations\n• Standard clauses for this document type\n• Signature blocks and verification`)
    } finally { setLoading(false) }
  }

  async function copyText() {
    await navigator.clipboard.writeText(result)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  function downloadTxt() {
    const blob = new Blob([result], { type: 'text/plain' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = `${docType.replace(/\s+/g, '_')}_Mizan.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-10">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: '#F0FBF5' }}>
            <Pen size={20} style={{ color: '#1A5C35' }} />
          </div>
          <div>
            <h1 className="font-display text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Legal Drafter</h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Generate professional legal documents under Pakistani law</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* Left — template selector + fields */}
          <div className="space-y-5">
            {/* Template grid */}
            <div>
              <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>SELECT DOCUMENT TYPE</p>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(TEMPLATES).map(([type, { icon, desc }]) => (
                  <button key={type} onClick={() => { setDocType(type); setFields({}); setResult('') }}
                    className={cn('flex items-start gap-2.5 px-3 py-2.5 rounded-xl text-left transition-all border')}
                    style={{
                      background:   docType === type ? 'var(--gold-light)' : 'var(--bg-card)',
                      borderColor:  docType === type ? 'var(--gold-border)' : 'var(--border-default)',
                    }}>
                    <span className="text-lg shrink-0">{icon}</span>
                    <div>
                      <p className="text-xs font-medium leading-tight" style={{ color: docType === type ? 'var(--warning)' : 'var(--text-primary)' }}>{type}</p>
                      <p className="text-[10px] leading-tight mt-0.5" style={{ color: 'var(--text-muted)' }}>{desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Fields */}
            <div className="card p-5 space-y-3">
              <p className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>FILL IN DETAILS — {docType}</p>
              {Object.entries(template.fields).map(([key, label]) => (
                <div key={key}>
                  <label className="block text-xs mb-1" style={{ color: 'var(--text-secondary)' }}>{label}</label>
                  {label.includes('Details') || label.includes('Facts') || label.includes('Obligations') || label.includes('Powers') ? (
                    <textarea rows={3} className="search-input resize-none w-full text-sm"
                      placeholder={`Enter ${label.toLowerCase()}…`}
                      value={fields[key] || ''}
                      onChange={e => setField(key, e.target.value)} />
                  ) : (
                    <input className="search-input w-full text-sm"
                      placeholder={`Enter ${label.toLowerCase()}…`}
                      value={fields[key] || ''}
                      onChange={e => setField(key, e.target.value)} />
                  )}
                </div>
              ))}

              <button onClick={handleDraft} disabled={loading}
                className="btn-primary w-full py-2.5 text-sm flex items-center justify-center gap-2 disabled:opacity-40 mt-2">
                {loading ? <><Loader2 size={14} className="animate-spin" />Drafting…</> : <><Pen size={14} />Generate {docType}</>}
              </button>
            </div>
          </div>

          {/* Right — output */}
          <div>
            {result ? (
              <div className="card p-5 h-full flex flex-col">
                <div className="flex items-center justify-between mb-3 shrink-0">
                  <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                    {template.icon} {docType}
                  </p>
                  <div className="flex gap-2">
                    <button onClick={copyText}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all"
                      style={{ background: 'var(--bg-muted)', color: 'var(--text-secondary)' }}>
                      {copied ? <><Check size={12} />Copied</> : <><Copy size={12} />Copy</>}
                    </button>
                    <button onClick={downloadTxt}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all"
                      style={{ background: 'var(--navy)', color: '#fff' }}>
                      <Download size={12} />Download
                    </button>
                  </div>
                </div>
                <div className="flex-1 overflow-y-auto">
                  <pre className="text-sm leading-relaxed whitespace-pre-wrap"
                    style={{ fontFamily: 'DM Sans, sans-serif', color: 'var(--text-primary)' }}>
                    {result}
                  </pre>
                </div>
                <p className="text-xs italic mt-4 shrink-0" style={{ color: 'var(--text-muted)' }}>
                  ⚠️ Review with a qualified Pakistani lawyer before use.
                </p>
              </div>
            ) : (
              <div className="card p-10 h-full flex flex-col items-center justify-center text-center"
                style={{ minHeight: '400px' }}>
                <span className="text-4xl mb-4">{template.icon}</span>
                <p className="text-sm font-medium mb-2" style={{ color: 'var(--text-primary)' }}>{docType}</p>
                <p className="text-xs max-w-xs" style={{ color: 'var(--text-muted)' }}>
                  Fill in the fields on the left and click Generate. Your document will appear here, ready to copy or download.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
