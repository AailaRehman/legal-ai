# ⚖️ Pakistani Legal AI — Phase 1 MVP

RAG-powered AI legal assistant for Pakistani law, built with LangChain + Groq + FAISS + Streamlit.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
The `.env` file is already set up with your API keys.

### 3. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
legal-ai/
├── app.py                          # Streamlit frontend
├── requirements.txt
├── .env                            # API keys & config
├── data/
│   ├── raw/                        # Put your PDF laws here
│   ├── processed/
│   └── vector_store/               # FAISS index (auto-created)
└── src/
    ├── ingestion/
    │   ├── document_loader.py      # PDF/TXT ingestion + chunking
    │   └── vector_store.py         # FAISS build/load/update
    └── rag/
        └── rag_chain.py            # RAG chain + citation + memory
```

---

## 💡 How to Use

1. **Upload legal documents** via sidebar (PDF/TXT)
2. Click **Process & Index Documents**
3. Select your **mode** (Citizen / Lawyer / Student)
4. **Ask questions** in English or Urdu

---

## 📚 Recommended Documents to Add

Download and upload these:
- Constitution of Pakistan (PDF)
- Pakistan Penal Code (PPC)
- Code of Criminal Procedure (CrPC)
- PECA Act
- Family Laws Ordinance

---

## 🏗️ Architecture

```
User Query
    ↓
Streamlit UI
    ↓
RAG Chain (LangChain)
    ↓
FAISS Vector Search → Retrieve Top-5 Relevant Law Chunks
    ↓
Groq LLM (Llama 3.3-70B) → Generate Cited Answer
    ↓
Display Answer + Sources
```

---

## 🔮 Coming in Phase 2
- OCR for scanned documents
- Legal document analyzer
- Legal drafting system
- Multilingual (Urdu) support
- Judgment search engine
