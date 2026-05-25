const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export type UserMode = 'citizen' | 'lawyer' | 'student'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  sources?: Source[]
  timestamp?: string
}

export interface Source {
  law: string
  section: string
  snippet: string
}

export interface ChatResponse {
  answer: string
  sources: Source[]
  session_id: string
}

export interface AnalysisResponse {
  summary: string
  risk_score: number
  risk_level: 'low' | 'medium' | 'high'
  risk_factors: string[]
  missing_clauses: string[]
  positive_points: string[]
  entities: {
    persons: string[]
    organizations: string[]
    dates: string[]
    amounts: string[]
    law_sections: string[]
  }
}

// ─── Chat ─────────────────────────────────────────────────────
export async function sendChatMessage(
  query: string,
  mode: UserMode,
  history: ChatMessage[],
  sessionId?: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, mode, history, session_id: sessionId }),
  })
  if (!res.ok) throw new Error(`Chat API error: ${res.status}`)
  return res.json()
}

export async function* streamChatMessage(
  query: string,
  mode: UserMode,
  history: ChatMessage[],
  sessionId?: string
): AsyncGenerator<string> {
  const res = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, mode, history, session_id: sessionId }),
  })
  if (!res.ok || !res.body) throw new Error(`Stream error: ${res.status}`)

  const reader = res.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value)
    // SSE lines: "data: <token>\n\n"
    const lines = chunk.split('\n').filter(l => l.startsWith('data: '))
    for (const line of lines) {
      const token = line.slice(6)
      if (token !== '[DONE]') yield token
    }
  }
}

// ─── Document Analysis ────────────────────────────────────────
export async function analyzeDocument(
  text: string,
  filename?: string
): Promise<AnalysisResponse> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, filename }),
  })
  if (!res.ok) throw new Error(`Analysis API error: ${res.status}`)
  return res.json()
}

// ─── Draft ────────────────────────────────────────────────────
export async function draftDocument(
  doc_type: string,
  fields: Record<string, string>
): Promise<{ content: string }> {
  const res = await fetch(`${API_BASE}/draft`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doc_type, fields }),
  })
  if (!res.ok) throw new Error(`Draft API error: ${res.status}`)
  return res.json()
}

// ─── Health ───────────────────────────────────────────────────
export async function checkHealth(): Promise<{ status: string; kb_ready: boolean }> {
  const res = await fetch(`${API_BASE}/health`)
  if (!res.ok) throw new Error('Health check failed')
  return res.json()
}
