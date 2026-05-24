'use client'

import { useState, useRef, useEffect } from 'react'
import { Navbar } from '@/components/layout/Navbar'
import { Scale, Send, Square, Globe, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Message {
  role: 'user' | 'assistant'
  content: string
  detectedLang?: string
  timestamp: string
}

const SAMPLE_QUERIES = [
  { ur: 'میرے مالک مکان نے مجھے بے دخل کرنے کی دھمکی دی ہے', en: 'Tenant rights' },
  { ur: 'ایف آئی آر کیسے درج کروائیں؟', en: 'FIR filing' },
  { ur: 'میری ملازمت ختم کر دی گئی ہے بغیر نوٹس کے', en: 'Job termination' },
  { ur: 'طلاق کے بعد بچوں کی تحویل کس کو ملتی ہے؟', en: 'Child custody' },
]

const LANG_OPTIONS = [
  { value: 'auto',  label: 'Auto-detect' },
  { value: 'urdu',  label: 'اردو' },
  { value: 'roman', label: 'Roman Urdu' },
  { value: 'en',    label: 'English' },
]

export default function MultilingualPage() {
  const [messages, setMessages]     = useState<Message[]>([])
  const [input, setInput]           = useState('')
  const [loading, setLoading]       = useState(false)
  const [lang, setLang]             = useState('auto')
  const bottomRef                   = useRef<HTMLDivElement>(null)
  const textareaRef                 = useRef<HTMLTextAreaElement>(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 160) + 'px'
  }, [input])

  function detectScript(text: string): string {
    const urduChars = (text.match(/[\u0600-\u06FF]/g) || []).length
    if (urduChars > 2) return 'urdu'
    const romanUrduWords = /\b(kya|hai|mera|tera|aur|nahi|hain|ka|ki|ke|se|ko|mein|pe|tha|thi|hy|ho|kar|karo)\b/i
    if (romanUrduWords.test(text)) return 'roman_urdu'
    return 'english'
  }

  async function sendMessage() {
    if (!input.trim() || loading) return
    const detectedLang = lang === 'auto' ? detectScript(input) : lang
    const userMsg: Message = {
      role: 'user', content: input, detectedLang, timestamp: new Date().toISOString()
    }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setInput('')
    setLoading(true)

    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/multilingual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, language: detectedLang, history: messages }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setMessages([...newMessages, {
        role: 'assistant', content: data.answer,
        detectedLang: data.response_language,
        timestamp: new Date().toISOString()
      }])
    } catch {
      const isUrdu = detectedLang === 'urdu'
      setMessages([...newMessages, {
        role: 'assistant',
        content: isUrdu
          ? `[بیک اینڈ کنیکٹ نہیں ہے]\n\nآپ کا سوال موصول ہوا: "${input}"\n\nجب FastAPI بیک اینڈ چل رہا ہوگا، تو آپ کو پاکستانی قانون کے حوالے سے مکمل جواب اردو میں ملے گا۔`
          : `[Backend not connected]\n\nYour query was received: "${input}"\n\nOnce FastAPI is running, you'll get answers in the same language you asked — Urdu, Roman Urdu, or English — grounded in Pakistani law.`,
        detectedLang: detectedLang,
        timestamp: new Date().toISOString()
      }])
    } finally { setLoading(false) }
  }

  const langLabel: Record<string, string> = {
    urdu: 'اردو', roman_urdu: 'Roman Urdu', english: 'English',
    auto: 'Auto', roman: 'Roman Urdu', en: 'English'
  }

  return (
    <div className="h-screen flex flex-col" style={{ background: 'var(--bg-page)' }}>
      <Navbar />

      <div className="flex-1 flex flex-col overflow-hidden max-w-3xl mx-auto w-full px-4 py-4">

        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ background: '#EEF1F8' }}>
              <Globe size={18} style={{ color: 'var(--navy)' }} />
            </div>
            <div>
              <h1 className="font-display text-lg font-semibold" style={{ color: 'var(--text-primary)' }}>Multilingual Legal Chat</h1>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>اردو · Roman Urdu · English — پاکستانی قانون</p>
            </div>
          </div>

          {/* Language selector */}
          <div className="flex gap-1 p-1 rounded-lg" style={{ background: 'var(--bg-muted)' }}>
            {LANG_OPTIONS.map(l => (
              <button key={l.value} onClick={() => setLang(l.value)}
                className="px-2.5 py-1.5 rounded-md text-xs transition-all"
                style={{
                  background: lang === l.value ? 'var(--bg-card)' : 'transparent',
                  color:      lang === l.value ? 'var(--text-primary)' : 'var(--text-muted)',
                  fontFamily: l.value === 'urdu' ? 'serif' : undefined,
                }}>{l.label}
              </button>
            ))}
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 pb-2">
          {messages.length === 0 ? (
            <div className="pt-6 space-y-4">
              <p className="text-center text-sm" style={{ color: 'var(--text-muted)' }}>
                آپ اردو، Roman Urdu، یا English میں سوال پوچھ سکتے ہیں<br />
                <span className="text-xs">Ask in any language — get answers in the same language</span>
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SAMPLE_QUERIES.map((q, i) => (
                  <button key={i} onClick={() => setInput(q.ur)}
                    className="card px-4 py-3 text-right hover:shadow-sm transition-all text-sm"
                    style={{ direction: 'rtl', fontFamily: 'serif', color: 'var(--text-primary)' }}>
                    {q.ur}
                    <span className="block text-xs mt-0.5 text-left" style={{ direction: 'ltr', color: 'var(--text-muted)', fontFamily: 'DM Sans, sans-serif' }}>
                      {q.en}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={cn('flex gap-3', msg.role === 'user' ? 'flex-row-reverse' : '')}>
                <div className={cn('w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5',
                  msg.role === 'user' ? '' : '')}
                  style={{ background: msg.role === 'user' ? 'var(--bg-muted)' : 'var(--navy)' }}>
                  {msg.role === 'user'
                    ? <span className="text-sm">👤</span>
                    : <Scale size={14} color="#C9A84C" />
                  }
                </div>
                <div className={cn('max-w-[80%]', msg.role === 'user' ? 'items-end' : '')}>
                  <div
                    className="px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap"
                    style={{
                      background:  msg.role === 'user' ? 'var(--chat-user-bg)' : 'var(--chat-ai-bg)',
                      color:       msg.role === 'user' ? 'var(--chat-user-fg)' : 'var(--chat-ai-fg)',
                      borderRadius: msg.role === 'user' ? '16px 16px 2px 16px' : '16px 16px 16px 2px',
                      direction:   msg.detectedLang === 'urdu' ? 'rtl' : 'ltr',
                      fontFamily:  msg.detectedLang === 'urdu' ? 'serif' : 'DM Sans, sans-serif',
                    }}
                  >
                    {msg.content}
                  </div>
                  {msg.detectedLang && (
                    <span className="text-[10px] mt-1 block px-1"
                      style={{ color: 'var(--text-muted)', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                      {langLabel[msg.detectedLang] || msg.detectedLang}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex gap-3 items-start">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: 'var(--navy)' }}>
                <Scale size={14} color="#C9A84C" />
              </div>
              <div className="px-4 py-3 rounded-2xl flex items-center gap-1.5" style={{ background: 'var(--chat-ai-bg)' }}>
                <div className="typing-dot" /><div className="typing-dot" /><div className="typing-dot" />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="pt-3 border-t" style={{ borderColor: 'var(--border-default)' }}>
          <div className="flex items-end gap-2 p-2 rounded-xl"
            style={{ background: 'var(--bg-card)', border: '0.5px solid var(--border-default)' }}>
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() }}}
              placeholder="اردو میں لکھیں یا Type in English / Roman Urdu..."
              rows={1}
              className="flex-1 bg-transparent outline-none resize-none text-sm leading-relaxed py-1 px-2"
              style={{ color: 'var(--text-primary)', fontFamily: 'DM Sans, sans-serif', minHeight: '36px' }}
            />
            {loading ? (
              <button onClick={() => setLoading(false)}
                className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
                style={{ background: '#FEF0F0', color: '#C0392B' }}>
                <Square size={14} fill="currentColor" />
              </button>
            ) : (
              <button onClick={sendMessage} disabled={!input.trim()}
                className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 disabled:opacity-30"
                style={{ background: 'var(--navy)', color: '#fff' }}>
                <Send size={14} />
              </button>
            )}
          </div>
          <p className="text-center text-[10px] mt-1.5" style={{ color: 'var(--text-muted)' }}>
            پاکستانی قانون پر مبنی — Grounded in Pakistani law · Not legal advice
          </p>
        </div>
      </div>
    </div>
  )
}
