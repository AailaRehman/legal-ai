"""
Pakistani Legal AI — Streamlit Frontend
Phase 1 MVP
"""

import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.document_loader import ingest_documents, ingest_single_file
from src.ingestion.vector_store import (
    build_vector_store,
    load_vector_store,
    add_documents_to_store,
    vector_store_exists,
)
from src.rag.rag_chain import create_rag_chain

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Pakistani Legal AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');

* { font-family: 'Source Sans Pro', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }

.main { background-color: #0f1117; }

.law-header {
    background: linear-gradient(135deg, #1a472a 0%, #0f2d1a 50%, #0a1f12 100%);
    border: 1px solid #2d6a4f;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.law-header h1 { color: #d4af37; font-size: 2.2rem; margin: 0; }
.law-header p { color: #a8c5a0; margin: 0.5rem 0 0 0; font-size: 1rem; }

.chat-user {
    background: linear-gradient(135deg, #1a3a2a, #0f2d1a);
    border-left: 3px solid #d4af37;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    color: #e8f5e9;
}
.chat-ai {
    background: linear-gradient(135deg, #0d1f1a, #0a1510);
    border-left: 3px solid #2d6a4f;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    color: #c8e6c9;
}
.source-badge {
    background: #1a3a2a;
    border: 1px solid #2d6a4f;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: #81c784;
    display: inline-block;
    margin: 2px;
}
.mode-info {
    background: #0d2818;
    border: 1px solid #2d6a4f;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #a8c5a0;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}
.stButton button {
    background: linear-gradient(135deg, #1a472a, #2d6a4f) !important;
    color: #d4af37 !important;
    border: 1px solid #2d6a4f !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #2d6a4f, #1a472a) !important;
    border-color: #d4af37 !important;
}
.disclaimer {
    background: #1a1a0d;
    border: 1px solid #5c5c00;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    color: #b3b300;
    font-size: 0.8rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────

def init_session():
    defaults = {
        "messages": [],
        "rag_chain": None,
        "vectorstore": None,
        "mode": "Citizen",
        "kb_loaded": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚖️ Pakistani Legal AI")
    st.markdown("---")

    # Mode selector
    st.markdown("### 🎭 Select Mode")
    mode = st.radio(
        "",
        ["Citizen", "Lawyer", "Student"],
        index=["Citizen", "Lawyer", "Student"].index(st.session_state.mode),
        help="Citizen: Simple language | Lawyer: Technical | Student: Academic"
    )

    mode_descriptions = {
        "Citizen": "🏠 Simple explanations for everyday people",
        "Lawyer": "⚖️ Technical sections, precedents & citations",
        "Student": "📚 Academic explanations with examples",
    }
    st.markdown(f'<div class="mode-info">{mode_descriptions[mode]}</div>', unsafe_allow_html=True)

    if mode != st.session_state.mode:
        st.session_state.mode = mode
        if st.session_state.rag_chain:
            st.session_state.rag_chain.set_mode(mode)

    st.markdown("---")

    # Knowledge Base section
    st.markdown("### 📚 Knowledge Base")

    # Load existing KB
    if not st.session_state.kb_loaded:
        if vector_store_exists():
            with st.spinner("Loading knowledge base..."):
                vs = load_vector_store()
                if vs:
                    st.session_state.vectorstore = vs
                    st.session_state.rag_chain = create_rag_chain(vs, st.session_state.mode)
                    st.session_state.kb_loaded = True
                    st.success("✅ Knowledge base loaded!")

    if st.session_state.kb_loaded:
        st.success("✅ Knowledge base ready")
    else:
        st.warning("⚠️ No knowledge base found. Upload documents below.")

    st.markdown("#### Upload Legal Documents")
    uploaded_files = st.file_uploader(
        "PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload Pakistani law documents, judgments, acts, etc.",
    )

    if uploaded_files and st.button("📥 Process & Index Documents"):
        all_docs = []
        with st.spinner("Processing documents..."):
            for uf in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uf.name).suffix) as tmp:
                    tmp.write(uf.read())
                    tmp_path = tmp.name

                docs = ingest_single_file(tmp_path)
                # Fix metadata source name
                for d in docs:
                    d.metadata["source"] = uf.name
                all_docs.extend(docs)
                os.unlink(tmp_path)

        if all_docs:
            with st.spinner("Building vector index..."):
                if st.session_state.vectorstore:
                    vs = add_documents_to_store(all_docs)
                else:
                    vs = build_vector_store(all_docs)

                st.session_state.vectorstore = vs
                st.session_state.rag_chain = create_rag_chain(vs, st.session_state.mode)
                st.session_state.kb_loaded = True

            st.success(f"✅ Indexed {len(all_docs)} chunks from {len(uploaded_files)} file(s)")
            st.rerun()
        else:
            st.error("Could not extract text. Try a different file.")

    st.markdown("---")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        if st.session_state.rag_chain:
            st.session_state.rag_chain.clear_memory()
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Supported Laws:**
    - 🇵🇰 Constitution of Pakistan
    - ⚖️ PPC / CrPC
    - 📋 Qanun-e-Shahadat
    - 💻 PECA (Cybercrime)
    - 👨‍👩‍👧 Family Laws
    - 👷 Labour Laws
    - 💰 Tax Laws
    - 📑 Court Judgments
    """)


# ── Main area ─────────────────────────────────────────────────────────────────

st.markdown("""
<div class="law-header">
    <h1>⚖️ Pakistani Legal AI Assistant</h1>
    <p>RAG-Powered • Citation-Grounded • Multilingual Legal Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Quick question suggestions
if not st.session_state.messages:
    st.markdown("### 💡 Try asking:")
    cols = st.columns(3)
    suggestions = [
        "What is the punishment for murder under PPC?",
        "How to file an FIR in Pakistan?",
        "What are my rights during arrest?",
        "Explain Section 302 PPC",
        "What is cybercrime punishment under PECA?",
        "How does bail work in Pakistan?",
    ]
    for i, col in enumerate(cols):
        with col:
            if st.button(suggestions[i * 2], key=f"s{i*2}"):
                st.session_state["quick_q"] = suggestions[i * 2]
            if i * 2 + 1 < len(suggestions):
                if st.button(suggestions[i * 2 + 1], key=f"s{i*2+1}"):
                    st.session_state["quick_q"] = suggestions[i * 2 + 1]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-user">🧑 <strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai">⚖️ <strong>Legal AI:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        if msg.get("sources"):
            st.markdown("**📚 Sources:**")
            for src in msg["sources"]:
                st.markdown(f'<span class="source-badge">📄 {src}</span>', unsafe_allow_html=True)
            st.markdown("")


# ── Chat input ────────────────────────────────────────────────────────────────

# Handle quick question
if "quick_q" in st.session_state:
    user_input = st.session_state.pop("quick_q")
else:
    user_input = None

chat_input = st.chat_input("Ask any question about Pakistani law... (English or Urdu)")
if chat_input:
    user_input = chat_input

if user_input:
    if not st.session_state.kb_loaded or not st.session_state.rag_chain:
        st.error("⚠️ Please upload and index legal documents first using the sidebar.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("⚖️ Searching legal knowledge base..."):
            result = st.session_state.rag_chain.ask(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        })
        st.rerun()


# ── Disclaimer ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="disclaimer">
⚠️ <strong>Disclaimer:</strong> This AI provides general legal information based on Pakistani law documents.
It is NOT a substitute for professional legal advice. Always consult a qualified lawyer for your specific situation.
</div>
""", unsafe_allow_html=True)
