# Mizan Deployment Guide

## Architecture
```
Frontend (Vercel)  ──►  Backend (Railway)  ──►  Groq API
     Next.js              FastAPI + FAISS         LLaMA 3.3
```

---

## Step 1 — Get your Groq API Key
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key → copy it

---

## Step 2 — Deploy Backend to Railway

1. Go to https://railway.app → New Project → Deploy from GitHub
2. Select repo: `AailaRehman/legal-ai`
3. Select branch: `nextjs-frontend`
4. Set **Root Directory** to `backend`
5. Add environment variables:
   ```
   GROQ_API_KEY=your_key_here
   JWT_SECRET=any-long-random-string-here
   ```
6. Railway will auto-detect Python and deploy
7. Copy your Railway URL: `https://your-app.railway.app`

**Test it:** Open `https://your-app.railway.app/health` → should return `{"status":"ok"}`

---

## Step 3 — Build the Knowledge Base

After backend is deployed, run this locally (or via Railway CLI):

```bash
cd backend
pip install -r requirements.txt
GROQ_API_KEY=your_key python scripts/build_kb.py
```

This ingests your 25 Pakistani law PDFs into FAISS.
Copy your `vector_store/` folder to the Railway deployment.

**Or** — run it via the Admin Panel once deployed:
- Log in as `admin / admin123`
- Go to Admin → KB Management → Build Knowledge Base

---

## Step 4 — Deploy Frontend to Vercel

1. Go to https://vercel.com → New Project → Import from GitHub
2. Select repo: `AailaRehman/legal-ai`
3. Select branch: `nextjs-frontend`
4. Set **Root Directory** to `.` (root)
5. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```
6. Click Deploy

Your app will be live at: `https://mizan-your-name.vercel.app`

---

## Step 5 — Test end-to-end

| Feature | Test |
|---------|------|
| Auth | Login with `lawyer1 / law12345` |
| Chat | Ask "What is bail under Pakistani law?" |
| Multilingual | Type "میرے حقوق کیا ہیں؟" |
| Strategy | Describe a landlord dispute |
| Education | Generate 5 MCQs on Constitutional Law |
| Analyze | Paste a contract, check risk score |
| Draft | Generate a Legal Notice |
| Admin | Login as `admin / admin123` → view analytics |

---

## Local Development

```bash
# Terminal 1 — Frontend
npm install
npm run dev          # http://localhost:3000

# Terminal 2 — Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY
python scripts/build_kb.py   # build KB once
uvicorn main:app --reload    # http://localhost:8000
```

## Environment Variables Summary

| Variable | Where | Value |
|----------|-------|-------|
| `GROQ_API_KEY` | Railway backend | From console.groq.com |
| `JWT_SECRET` | Railway backend | Any random string (32+ chars) |
| `NEXT_PUBLIC_API_URL` | Vercel frontend | Your Railway URL |
