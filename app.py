"""
Pakistani Legal AI — Streamlit Frontend
Phase 1 MVP — Premium UI Redesign
"""

import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

_project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_project_root / ".env")

from src.ingestion.document_loader import ingest_documents, ingest_single_file
from src.ingestion.vector_store import (
    build_vector_store, load_vector_store,
    add_documents_to_store, vector_store_exists,
)
from src.rag.rag_chain import create_rag_chain
from src.auth.auth_manager import init_auth, require_auth, get_current_user, get_role_info, logout
from src.auth.auth_ui import render_auth_page
from src.database.db_manager import save_message, get_chat_history, init_db

# ── Init DB
init_db()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mizan — Pakistani Legal AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0A0C0F !important;
    color: #E8E4DC !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1400px !important; }

[data-testid="stSidebar"] {
    background: #0D1017 !important;
    border-right: 1px solid #1E2530 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.5rem !important; }

.sidebar-brand {
    display: flex; align-items: center; gap: 0.75rem;
    padding-bottom: 1.5rem; border-bottom: 1px solid #1E2530; margin-bottom: 1.5rem;
}
.sidebar-brand-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #C9A84C, #8B6914);
    border-radius: 10px; display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; flex-shrink: 0;
}
.sidebar-brand-text h2 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.3rem !important; font-weight: 600 !important;
    color: #C9A84C !important; line-height: 1.1;
}
.sidebar-brand-text p {
    font-size: 0.7rem !important; color: #5A6478 !important;
    letter-spacing: 0.08em; text-transform: uppercase;
}

.sidebar-section-label {
    font-size: 0.65rem !important; font-weight: 600 !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    color: #3D4A5C !important; margin: 1.5rem 0 0.75rem 0 !important;
}

[data-testid="stRadio"] label {
    font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important;
    color: #8A95A8 !important; padding: 0.35rem 0 !important; cursor: pointer;
}

.mode-pill {
    border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.8rem;
    color: #8A95A8; border: 1px solid #1E2530; background: #111620;
    margin-bottom: 1.5rem; line-height: 1.5;
}
.mode-pill strong { color: #C9A84C; display: block; margin-bottom: 0.2rem; }

.kb-status-ok {
    display: flex; align-items: center; gap: 0.5rem;
    background: #0C1F14; border: 1px solid #1A3828; border-radius: 8px;
    padding: 0.65rem 0.9rem; font-size: 0.8rem; color: #4CAF7D; margin-bottom: 0.75rem;
}
.kb-status-warn {
    display: flex; align-items: center; gap: 0.5rem;
    background: #1A1408; border: 1px solid #3D2E0A; border-radius: 8px;
    padding: 0.65rem 0.9rem; font-size: 0.8rem; color: #C9A84C; margin-bottom: 0.75rem;
}

.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1A2235, #111827) !important;
    color: #C9A84C !important; border: 1px solid #2A3650 !important;
    border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 0.6rem 1rem !important; letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #C9A84C22, #C9A84C11) !important;
    border-color: #C9A84C88 !important; color: #E8C96A !important;
}

.hero {
    position: relative; padding: 3.5rem 3rem 2.5rem;
    margin: 1.5rem 0 2rem; border-radius: 16px;
    background: linear-gradient(135deg, #0F1A0F 0%, #0D1520 40%, #0A0C0F 100%);
    border: 1px solid #1E2A1E; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, #C9A84C18 0%, transparent 70%);
}
.hero::after {
    content: ''; position: absolute; bottom: -40px; left: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, #2D6A4F18 0%, transparent 70%);
}
.hero-eyebrow {
    font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: #C9A84C; margin-bottom: 0.75rem; font-weight: 500;
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3.2rem !important; font-weight: 300 !important;
    color: #E8E4DC !important; line-height: 1.1 !important; margin-bottom: 0.5rem !important;
}
.hero h1 em { font-style: italic; color: #C9A84C; }
.hero-sub { font-size: 0.9rem; color: #5A6478; letter-spacing: 0.03em; margin-top: 0.5rem; }
.hero-badges { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 1.5rem; }
.hero-badge {
    background: #1A2235; border: 1px solid #2A3650; border-radius: 20px;
    padding: 0.3rem 0.8rem; font-size: 0.72rem; color: #7A8BA0; letter-spacing: 0.04em;
}

.stats-bar {
    display: flex; gap: 1px; background: #1E2530;
    border-radius: 10px; overflow: hidden; margin-bottom: 2rem; border: 1px solid #1E2530;
}
.stat-item { flex: 1; padding: 1rem 1.25rem; background: #0D1017; text-align: center; }
.stat-num {
    font-family: 'DM Mono', monospace; font-size: 1.4rem;
    color: #C9A84C; font-weight: 500; display: block;
}
.stat-label {
    font-size: 0.68rem; color: #3D4A5C; text-transform: uppercase;
    letter-spacing: 0.1em; display: block; margin-top: 0.2rem;
}

.suggestions-label {
    font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase;
    color: #3D4A5C; margin-bottom: 1rem; font-weight: 600;
}

.msg-user { display: flex; gap: 1rem; margin: 1.25rem 0; align-items: flex-start; }
.msg-ai { display: flex; gap: 1rem; margin: 1.25rem 0; align-items: flex-start; }
.msg-avatar {
    width: 34px; height: 34px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0; margin-top: 2px;
}
.msg-avatar-user { background: #1A2235; border: 1px solid #2A3650; color: #8A95A8; }
.msg-avatar-ai {
    background: linear-gradient(135deg, #1A3020, #0C1F14);
    border: 1px solid #1A3828; color: #4CAF7D;
}
.msg-bubble-user {
    background: #111620; border: 1px solid #1E2530;
    border-radius: 12px 12px 12px 3px; padding: 0.9rem 1.1rem;
    font-size: 0.9rem; color: #C8CDD8; line-height: 1.65; max-width: 85%;
}
.msg-bubble-ai {
    background: #0C1310; border: 1px solid #1A2E1E;
    border-radius: 12px 12px 3px 12px; padding: 0.9rem 1.1rem;
    font-size: 0.9rem; color: #D4DCC8; line-height: 1.75; max-width: 90%;
}
.sources-row {
    display: flex; flex-wrap: wrap; gap: 0.4rem;
    margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #1A2E1E;
}
.source-chip {
    background: #111820; border: 1px solid #1E2A30; border-radius: 6px;
    padding: 0.2rem 0.6rem; font-size: 0.7rem; color: #4A7A8A;
    font-family: 'DM Mono', monospace;
}

.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent);
    margin: 1.5rem 0;
}

.disclaimer {
    background: #0D1017; border: 1px solid #1E2530;
    border-left: 3px solid #C9A84C44; border-radius: 8px;
    padding: 0.8rem 1.1rem; font-size: 0.75rem; color: #3D4A5C;
    margin-top: 2rem; line-height: 1.6;
}
.disclaimer strong { color: #C9A84C88; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0A0C0F; }
::-webkit-scrollbar-thumb { background: #1E2530; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
def init_session():
    for k, v in {"messages": [], "rag_chain": None, "vectorstore": None,
                 "mode": "Citizen", "kb_loaded": False}.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Auth gate ──────────────────────────────────────────────────────────────────
init_auth()
if not require_auth():
    render_auth_page()
    st.stop()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    user = get_current_user()
    role_info = get_role_info(user.get("role","citizen"))
    st.markdown(f"""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">⚖️</div>
        <div class="sidebar-brand-text">
            <h2>Mizan</h2>
            <p>{role_info['icon']} {user.get('username','User')} · <span style="color:{role_info['color']}">{role_info['label']}</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-label">Consultation Mode</p>', unsafe_allow_html=True)
    mode = st.radio("", ["Citizen", "Lawyer", "Student"],
        index=["Citizen", "Lawyer", "Student"].index(st.session_state.mode),
        label_visibility="collapsed")

    mode_info = {
        "Citizen": ("Everyday Language", "Clear, jargon-free explanations for the general public."),
        "Lawyer": ("Technical & Precise", "Full citations, precedents, and statutory references."),
        "Student": ("Academic Mode", "Conceptual explanations with examples and context."),
    }
    title, desc = mode_info[mode]
    st.markdown(f'<div class="mode-pill"><strong>{title}</strong>{desc}</div>', unsafe_allow_html=True)

    if mode != st.session_state.mode:
        st.session_state.mode = mode
        if st.session_state.rag_chain:
            st.session_state.rag_chain.set_mode(mode)

    st.markdown('<p class="sidebar-section-label">Knowledge Base</p>', unsafe_allow_html=True)

    if not st.session_state.kb_loaded and vector_store_exists():
        with st.spinner("Loading..."):
            vs = load_vector_store()
            if vs:
                st.session_state.vectorstore = vs
                st.session_state.rag_chain = create_rag_chain(vs, st.session_state.mode)
                st.session_state.kb_loaded = True

    if st.session_state.kb_loaded:
        st.markdown('<div class="kb-status-ok">✦ &nbsp;25 laws · 10,977 chunks · Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="kb-status-warn">⚠ &nbsp;Run build_index.py first</div>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-label">Add Documents</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"],
        accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files and st.button("⊕  Index Documents"):
        all_docs = []
        with st.spinner("Processing..."):
            for uf in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uf.name).suffix) as tmp:
                    tmp.write(uf.read())
                    tmp_path = tmp.name
                docs = ingest_single_file(tmp_path)
                for d in docs:
                    d.metadata["source"] = uf.name
                all_docs.extend(docs)
                os.unlink(tmp_path)
        if all_docs:
            with st.spinner("Building index..."):
                vs = add_documents_to_store(all_docs) if st.session_state.vectorstore else build_vector_store(all_docs)
                st.session_state.vectorstore = vs
                st.session_state.rag_chain = create_rag_chain(vs, st.session_state.mode)
                st.session_state.kb_loaded = True
            st.success(f"{len(all_docs)} chunks indexed")
            st.rerun()
        else:
            st.error("Could not extract text from file.")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if st.button("🚪  Sign Out"):
        logout()
        st.rerun()
    if st.button("↺  Clear Conversation"):
        st.session_state.messages = []
        if st.session_state.rag_chain:
            st.session_state.rag_chain.clear_memory()
        st.rerun()

    st.markdown('<p class="sidebar-section-label">Indexed Laws</p>', unsafe_allow_html=True)
    for law in ["Constitution of Pakistan", "Pakistan Penal Code", "Code of Criminal Procedure",
                "Qanun-e-Shahadat", "PECA 2016", "Anti-Terrorism Act", "Anti-Money Laundering Act",
                "Family Laws Ordinance", "Companies Act 2017", "Contract Act 1872",
                "Income Tax Ordinance", "Industrial Relations Act", "Transfer of Property Act",
                "Narcotics Control Act", "+ 11 more acts"]:
        st.markdown(f'<div style="font-size:0.73rem;color:#3D4A5C;padding:0.22rem 0;border-bottom:1px solid #0F1520">◦ {law}</div>', unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">⚖ &nbsp; AI Legal Intelligence · Pakistan</div>
    <h1>The Law,<br><em>Understood.</em></h1>
    <p class="hero-sub">RAG-powered · Citation-grounded · Bilingual English & Urdu</p>
    <div class="hero-badges">
        <span class="hero-badge">🇵🇰 Pakistani Law</span>
        <span class="hero-badge">📄 25 Legal Documents</span>
        <span class="hero-badge">🔍 10,977 Indexed Chunks</span>
        <span class="hero-badge">⚡ Groq LLaMA 3.3-70B</span>
        <span class="hero-badge">🧠 FAISS Semantic Search</span>
        <span class="hero-badge">⚖️ 15 SC Judgments</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item"><span class="stat-num">25</span><span class="stat-label">Legal Documents</span></div>
    <div class="stat-item"><span class="stat-num">10,977</span><span class="stat-label">Indexed Chunks</span></div>
    <div class="stat-item"><span class="stat-num">15</span><span class="stat-label">SC Judgments</span></div>
    <div class="stat-item"><span class="stat-num">3</span><span class="stat-label">User Modes</span></div>
    <div class="stat-item"><span class="stat-num">2</span><span class="stat-label">Languages</span></div>
</div>
""", unsafe_allow_html=True)

# ── Suggestions ────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown('<p class="suggestions-label">▸ &nbsp;Suggested questions</p>', unsafe_allow_html=True)
    suggestions = [
        ("⚖️", "What is the punishment for murder under Section 302 PPC?"),
        ("🚔", "What are my fundamental rights during arrest in Pakistan?"),
        ("💻", "What is the punishment for cybercrime under PECA 2016?"),
        ("📋", "How do I file an FIR in Pakistan? Step by step."),
        ("👨‍⚖️", "How does the bail process work in Pakistan?"),
        ("💍", "What are the grounds for divorce (Khula) in Pakistan?"),
    ]
    cols = st.columns(3)
    for i, (icon, q) in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(f"{icon}  {q}", key=f"sug_{i}"):
                st.session_state["quick_q"] = q

# ── Chat messages ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-avatar msg-avatar-user">👤</div>
            <div class="msg-bubble-user">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        chips = "".join(f'<span class="source-chip">📄 {s}</span>' for s in msg.get("sources", []))
        sources_html = f'<div class="sources-row">{chips}</div>' if chips else ""
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-avatar msg-avatar-ai">⚖️</div>
            <div class="msg-bubble-ai">
                {msg["content"].replace(chr(10), "<br>")}
                {sources_html}
            </div>
        </div>""", unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────────────
user_input = st.session_state.pop("quick_q", None)
chat_input = st.chat_input("Ask anything about Pakistani law — in English or Urdu...")
if chat_input:
    user_input = chat_input

if user_input:
    if not st.session_state.kb_loaded or not st.session_state.rag_chain:
        st.error("⚠️ Knowledge base not loaded. Run build_index.py first, then restart the app.")
    else:
        user = get_current_user()
        uid = user.get("id") if user else None
        sid = st.session_state.get("session_id", "default")
        mode = st.session_state.get("mode", "Citizen")

        st.session_state.messages.append({"role": "user", "content": user_input})
        if uid:
            save_message(uid, sid, "user", user_input, mode)

        with st.spinner("Searching legal knowledge base..."):
            result = st.session_state.rag_chain.ask(user_input)
        st.session_state.messages.append({
            "role": "assistant", "content": result["answer"], "sources": result["sources"],
        })
        if uid:
            save_message(uid, sid, "assistant", result["answer"], mode)
        st.rerun()

# ── Disclaimer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    <strong>Legal Disclaimer</strong> &nbsp;·&nbsp;
    Mizan provides general legal information based on Pakistani statutory law and is not a substitute
    for professional legal advice. Always consult a qualified advocate for matters specific to your situation.
    AI-generated responses may contain errors — verify critical information against primary sources.
</div>
""", unsafe_allow_html=True)
