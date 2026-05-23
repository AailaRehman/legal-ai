'use client'

import { useState, useCallback, useRef } from 'react'
import type { ChatMessage, UserMode } from '@/lib/api'

export interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  mode: UserMode
  sessionId: string | null
}

export function useChat() {
  const [messages, setMessages]   = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [mode, setMode]           = useState<UserMode>('citizen')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const abortRef                  = useRef<AbortController | null>(null)

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMsg: ChatMessage = {
      role:      'user',
      content,
      timestamp: new Date().toISOString(),
    }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setIsLoading(true)

    // Placeholder AI message for streaming
    const aiMsg: ChatMessage = {
      role:      'assistant',
      content:   '',
      sources:   [],
      timestamp: new Date().toISOString(),
    }
    setMessages([...newMessages, aiMsg])

    try {
      abortRef.current = new AbortController()

      // ── Call the FastAPI backend ──────────────────────────────
      const res = await fetch(
        (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/chat',
        {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify({
            query:      content,
            mode,
            history:    messages,
            session_id: sessionId,
          }),
          signal: abortRef.current.signal,
        }
      )

      if (!res.ok) throw new Error(`API error ${res.status}`)
      const data = await res.json()

      const finalMsg: ChatMessage = {
        role:      'assistant',
        content:   data.answer || 'Sorry, I could not get a response.',
        sources:   data.sources || [],
        timestamp: new Date().toISOString(),
      }
      if (data.session_id) setSessionId(data.session_id)

      setMessages([...newMessages, finalMsg])
    } catch (err: unknown) {
      if (err instanceof Error && err.name === 'AbortError') return

      // ── Fallback demo response (until backend is ready) ───────
      const fallback: ChatMessage = {
        role:    'assistant',
        content: `[Backend not connected yet]\n\nYou asked: "${content}"\n\nOnce the FastAPI backend is running at ${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}, real answers will appear here with citations from Pakistani law.`,
        sources: [],
        timestamp: new Date().toISOString(),
      }
      setMessages([...newMessages, fallback])
    } finally {
      setIsLoading(false)
    }
  }, [messages, mode, sessionId, isLoading])

  const clearChat = useCallback(() => {
    setMessages([])
    setSessionId(null)
  }, [])

  const stopGeneration = useCallback(() => {
    abortRef.current?.abort()
    setIsLoading(false)
  }, [])

  return {
    messages,
    isLoading,
    mode,
    setMode,
    sessionId,
    sendMessage,
    clearChat,
    stopGeneration,
  }
}
