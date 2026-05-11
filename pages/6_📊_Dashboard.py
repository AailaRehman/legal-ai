"""
Page 6: User Dashboard
Chat history, saved documents, saved analyses, saved strategies.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.auth.auth_manager import init_auth, require_auth, get_current_user, get_role_info
from src.auth.auth_ui import render_auth_page
from src.database.db_manager import (
    get_user_sessions, get_chat_history, delete_session,
    get_saved_documents, delete_document,
    get_saved_analyses, get_saved_strategies,
)

st.set_page_config(page_title="Dashboard — Mizan", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap');
html, body, .stApp { background: #0A0C0F !important; color: #E8E4DC !important; font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1200px !important; }

.page-eyebrow { font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.5rem; }
.page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 300; color: #E8E4DC; line-height: 1.1; margin-bottom: 0.4rem; }
.page-title em { font-style: italic; color: #C9A84C; }
.page-sub { font-size: 0.85rem; color: #5A6478; margin-bottom: 2rem; }

.stat-card {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 10px;
    padding: 1.25rem; text-align: center;
}
.stat-card-num { font-family: 'DM Mono', monospace; font-size: 2rem; color: #C9A84C; display: block; }
.stat-card-label { font-size: 0.7rem; color: #3D4A5C; text-transform: uppercase; letter-spacing: 0.1em; }

.session-card {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 10px;
    padding: 1rem 1.25rem; margin-bottom: 0.6rem; display: flex;
    justify-content: space-between; align-items: center;
}
.session-meta { font-size: 0.72rem; color: #3D4A5C; margin-top: 0.2rem; }
.session-title { font-size: 0.88rem; color: #C8CDD8; }

.doc-card {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 10px;
    padding: 1rem 1.25rem; margin-bottom: 0.6rem;
}
.doc-type-badge {
    display: inline-block; background: #1A1A08; border: 1px solid #2A2A18;
    border-radius: 5px; padding: 0.15rem 0.5rem; font-size: 0.7rem; color: #C9A84C;
    margin-bottom: 0.4rem;
}
.doc-title { font-size: 0.88rem; color: #C8CDD8; margin-bottom: 0.25rem; }
.doc-meta { font-size: 0.72rem; color: #3D4A5C; }

.msg-preview {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 8px;
    padding: 0.7rem 0.9rem; font-size: 0.8rem; color: #8A95A8;
    line-height: 1.6; margin: 0.3rem 0;
}
.msg-role-user { border-left: 2px solid #2A3650; }
.msg-role-ai { border-left: 2px solid #1A3828; }

.stButton > button {
    background: #0D1017 !important; color: #5A6478 !important;
    border: 1px solid #1E2530 !important; border-radius: 6px !important;
    font-size: 0.75rem !important; padding: 0.3rem 0.7rem !important;
}
.stButton > button:hover { border-color: #CF6679 !important; color: #CF6679 !important; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #1E2530; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

init_auth()

if not require_auth():
    render_auth_page()
    st.stop()

user = get_current_user()
role_info = get_role_info(user.get("role", "citizen"))

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-eyebrow">📊 &nbsp; Module 8 · Phase 4</div>
<div class="page-title">My <em>Dashboard</em></div>
<div class="page-sub">
    {role_info['icon']} {user.get('username','User')} &nbsp;·&nbsp;
    <span style="color:{role_info['color']}">{role_info['label']}</span> &nbsp;·&nbsp;
    {user.get('email','')}
</div>
""", unsafe_allow_html=True)

# ── Stats row ──────────────────────────────────────────────────────────────────
sessions     = get_user_sessions(user["id"])
documents    = get_saved_documents(user["id"])
analyses     = get_saved_analyses(user["id"])
strategies   = get_saved_strategies(user["id"])

cols = st.columns(4)
for col, (num, label) in zip(cols, [
    (len(sessions),   "Chat Sessions"),
    (len(documents),  "Saved Drafts"),
    (len(analyses),   "Saved Analyses"),
    (len(strategies), "Saved Strategies"),
]):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-card-num">{num}</span>
            <span class="stat-card-label">{label}</span>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat History", "📄 Saved Drafts", "🔍 Saved Analyses", "⚖️ Saved Strategies"])

# Tab 1: Chat History
with tab1:
    if not sessions:
        st.markdown('<div style="color:#3D4A5C;font-size:0.85rem;text-align:center;padding:2rem">No chat history yet. Start a conversation on the main page.</div>', unsafe_allow_html=True)
    else:
        for sess in sessions:
            sid = sess["session_id"]
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="session-card">
                    <div>
                        <div class="session-title">Session {sid} &nbsp;<span style="font-size:0.72rem;color:#C9A84C">[{sess.get('mode','Citizen')}]</span></div>
                        <div class="session-meta">
                            {sess.get('message_count',0)} messages &nbsp;·&nbsp;
                            Started: {sess.get('started_at','')[:16]} &nbsp;·&nbsp;
                            Last: {sess.get('last_message','')[:16]}
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with col2:
                if st.button("View", key=f"view_{sid}"):
                    st.session_state[f"expand_{sid}"] = not st.session_state.get(f"expand_{sid}", False)
                if st.button("🗑", key=f"del_{sid}"):
                    delete_session(user["id"], sid)
                    st.rerun()

            if st.session_state.get(f"expand_{sid}"):
                msgs = get_chat_history(user["id"], sid)
                for msg in msgs[-10:]:
                    role_class = "msg-role-user" if msg["role"] == "user" else "msg-role-ai"
                    icon = "👤" if msg["role"] == "user" else "⚖️"
                    preview = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
                    st.markdown(f'<div class="msg-preview {role_class}">{icon} {preview}</div>', unsafe_allow_html=True)

# Tab 2: Saved Drafts
with tab2:
    if not documents:
        st.markdown('<div style="color:#3D4A5C;font-size:0.85rem;text-align:center;padding:2rem">No saved drafts yet. Generate documents from the Legal Drafter page.</div>', unsafe_allow_html=True)
    else:
        for doc in documents:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="doc-card">
                    <span class="doc-type-badge">{doc['doc_type']}</span>
                    <div class="doc-title">{doc['title']}</div>
                    <div class="doc-meta">Saved: {doc['created_at'][:16]}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.download_button("⬇", data=doc["content"],
                    file_name=f"{doc['title']}.txt", mime="text/plain",
                    key=f"dl_doc_{doc['id']}")
                if st.button("🗑", key=f"del_doc_{doc['id']}"):
                    delete_document(user["id"], doc["id"])
                    st.rerun()

# Tab 3: Saved Analyses
with tab3:
    if not analyses:
        st.markdown('<div style="color:#3D4A5C;font-size:0.85rem;text-align:center;padding:2rem">No saved analyses yet. Analyze documents and save results from the Document Analyzer page.</div>', unsafe_allow_html=True)
    else:
        for an in analyses:
            risk = an.get("risk_score", 0)
            risk_color = "#4CAF7D" if risk < 40 else "#C9A84C" if risk < 70 else "#CF6679"
            st.markdown(f"""
            <div class="doc-card">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div class="doc-title">📄 {an['filename']}</div>
                    <span style="font-family:'DM Mono',monospace;font-size:1.1rem;color:{risk_color}">Risk: {risk}</span>
                </div>
                <div class="doc-meta">Analyzed: {an['created_at'][:16]}</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("View Analysis"):
                st.text(an["analysis"][:1000] + "..." if len(an["analysis"]) > 1000 else an["analysis"])
                st.download_button("⬇ Download", data=an["analysis"],
                    file_name=f"analysis_{an['filename']}.txt", mime="text/plain",
                    key=f"dl_an_{an['id']}")

# Tab 4: Saved Strategies
with tab4:
    if not strategies:
        st.markdown('<div style="color:#3D4A5C;font-size:0.85rem;text-align:center;padding:2rem">No saved strategies yet. Generate legal strategies from the Case Strategy page.</div>', unsafe_allow_html=True)
    else:
        for strat in strategies:
            st.markdown(f"""
            <div class="doc-card">
                <div class="doc-title">⚖️ {strat['title']}</div>
                <div class="doc-meta" style="margin-top:0.3rem;color:#5A6478">
                    {strat['situation'][:100]}...
                </div>
                <div class="doc-meta">Saved: {strat['created_at'][:16]}</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("View Strategy"):
                st.text(strat["strategy"][:1000] + "..." if len(strat["strategy"]) > 1000 else strat["strategy"])
                st.download_button("⬇ Download", data=strat["strategy"],
                    file_name=f"strategy_{strat['id']}.txt", mime="text/plain",
                    key=f"dl_st_{strat['id']}")
