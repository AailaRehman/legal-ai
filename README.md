# Mizan — Pakistan Legal AI

> AI-powered legal intelligence grounded in Pakistani law. Built with Next.js 14 + FastAPI + RAG.

## Stack

| Layer    | Tech |
|----------|------|
| Frontend | Next.js 14 (App Router) · Tailwind CSS · Framer Motion |
| Backend  | FastAPI (Python) · LangChain · Groq LLaMA 3.3-70B |
| Vector DB| FAISS · HuggingFace `all-MiniLM-L6-v2` |
| Database | PostgreSQL (prod) / SQLite (dev) |

## Project Structure

```
src/
  app/
    page.tsx          ← Landing page
    chat/page.tsx     ← Core chat product
    analyze/page.tsx  ← Document analyzer
    draft/page.tsx    ← Legal drafter
    research/page.tsx ← Law research
    dashboard/page.tsx
  components/
    layout/           ← Navbar, Footer
    landing/          ← Hero, Features, ChatPreview, StatsBar
    chat/             ← ChatMessage, ChatInput, ChatSidebar
    ui/               ← ThemeToggle
  hooks/
    useChat.ts        ← Chat state + API calls
  lib/
    api.ts            ← FastAPI client
    utils.ts          ← cn() helper
  styles/
    globals.css       ← Design tokens (light + dark)
```

## Getting Started

```bash
# 1. Install dependencies
npm install

# 2. Set up environment
cp .env.local.example .env.local
# Edit NEXT_PUBLIC_API_URL to point to your FastAPI server

# 3. Run dev server
npm run dev
# Open http://localhost:3000
```

## Design Tokens

Colors defined as CSS variables in `globals.css`:

| Token | Light | Dark |
|-------|-------|------|
| `--gold` | `#C9A84C` | `#C9A84C` |
| `--navy` | `#1A2744` | `#1A2744` |
| `--bg-page` | `#F7F6F2` | `#0F1218` |
| `--bg-card` | `#FFFFFF` | `#181D28` |
| `--text-primary` | `#1A1917` | `#EDE9E0` |

## Connecting the Backend

The frontend expects a FastAPI server at `NEXT_PUBLIC_API_URL`. See `/backend` for the FastAPI setup (next step).

Key endpoints:
- `POST /chat` → `{ answer, sources, session_id }`
- `POST /analyze` → `{ summary, risk_score, risk_factors, ... }`
- `POST /draft` → `{ content }`
- `GET /health` → `{ status, kb_ready }`

## Roadmap

- [x] Landing page (Hero, Features, ChatPreview)
- [x] Chat page (messages, sidebar, mode selector, empty state)
- [x] Light/dark theme toggle
- [ ] FastAPI backend + RAG engine
- [ ] Document analyzer page (full)
- [ ] Legal drafter page (full)
- [ ] Auth system
- [ ] Dashboard with saved history
