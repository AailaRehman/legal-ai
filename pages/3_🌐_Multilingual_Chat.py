"""
Page 3: Multilingual Legal Chat
Ask legal questions in English, Urdu, or Roman Urdu.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.multilingual import detect_language, translate_to_urdu, translate_to_roman_urdu, translate_to_english
from src.ingestion.vector_store import load_vector_store, vector_store_exists
from src.rag.rag_chain import create_rag_chain

st.set_page_config(page_title="Multilingual — Mizan", page_icon="🌐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=Noto+Nastaliq+Urdu&display=swap');
html, body, .stApp { background: #0A0C0F !important; color: #E8E4DC !important; font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1100px !important; }

.page-eyebrow { font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.5rem; }
.page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 300; color: #E8E4DC; line-height: 1.1; margin-bottom: 0.4rem; }
.page-title em { font-style: italic; color: #C9A84C; }
.page-sub { font-size: 0.85rem; color: #5A6478; margin-bottom: 2rem; }

.lang-bar {
    display: flex; gap: 0.5rem; margin-bottom: 1.5rem; flex-wrap: wrap;
}
.lang-chip {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 20px;
    padding: 0.3rem 0.9rem; font-size: 0.78rem; color: #5A6478;
}
.lang-chip.active { border-color: #C9A84C; color: #C9A84C; background: #1A1A08; }

.detected-lang {
    background: #0C1F14; border: 1px solid #1A3828; border-radius: 8px;
    padding: 0.5rem 0.9rem; font-size: 0.78rem; color: #4CAF7D;
    margin-bottom: 1rem; display: inline-block;
}

.msg-user {
    display: flex; gap: 0.75rem; margin: 1rem 0; align-items: flex-start;
}
.msg-ai { display: flex; gap: 0.75rem; margin: 1rem 0; align-items: flex-start; }
.msg-avatar {
    width: 32px; height: 32px; border-radius: 8px; display: flex;
    align-items: center; justify-content: center; font-size: 0.8rem; flex-shrink: 0;
}
.msg-avatar-user { background: #1A2235; border: 1px solid #2A3650; }
.msg-avatar-ai { background: #0C1F14; border: 1px solid #1A3828; }
.msg-bubble-user {
    background: #111620; border: 1px solid #1E2530; border-radius: 10px 10px 10px 2px;
    padding: 0.8rem 1rem; font-size: 0.88rem; color: #C8CDD8; line-height: 1.65; max-width: 80%;
}
.msg-bubble-ai {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 10px 10px 2px 10px;
    padding: 0.8rem 1rem; font-size: 0.88rem; color: #D4DCC8; line-height: 1.8; max-width: 85%;
}
.msg-bubble-urdu {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 10px;
    padding: 0.8rem 1rem; font-size: 1rem; color: #D4DCC8; line-height: 2;
    max-width: 85%; direction: rtl; text-align: right;
    font-family: 'Noto Nastaliq Urdu', serif;
}
.lang-badge {
    display: inline-block; font-size: 0.65rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: #3D4A5C; border: 1px solid #1E2530;
    border-radius: 4px; padding: 0.1rem 0.4rem; margin-right: 0.4rem;
}
.stButton > button {
    background: linear-gradient(135deg, #1A2235, #111827) !important;
    color: #C9A84C !important; border: 1px solid #2A3650 !important;
    border-radius: 8px !important; font-size: 0.82rem !important; font-weight: 500 !important;
}
[data-testid="stChatInput"] textarea { color: #C8CDD8 !important; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-eyebrow">🌐 &nbsp; Module 4 · Phase 3</div>
<div class="page-title">Multilingual Legal <em>Chat</em></div>
<div class="page-sub">Ask in English · اردو · Roman Urdu — AI understands and responds in your language</div>
""", unsafe_allow_html=True)

# ── Language bar ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="lang-bar">
    <span class="lang-chip active">🇬🇧 English</span>
    <span class="lang-chip active">🇵🇰 اردو Urdu</span>
    <span class="lang-chip active">🗣️ Roman Urdu</span>
</div>
""", unsafe_allow_html=True)

# ── Output language selector ───────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    output_lang = st.selectbox(
        "Response Language",
        ["Auto-detect (match input)", "English", "Urdu (اردو)", "Roman Urdu"],
        label_visibility="visible",
    )
with col2:
    if st.button("↺ Clear Chat"):
        st.session_state.multi_messages = []
        st.rerun()

lang_map = {
    "Auto-detect (match input)": "auto",
    "English": "english",
    "Urdu (اردو)": "urdu",
    "Roman Urdu": "roman_urdu",
}
selected_output_lang = lang_map[output_lang]

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Load RAG chain ─────────────────────────────────────────────────────────────
if "multi_rag" not in st.session_state:
    if vector_store_exists():
        vs = load_vector_store()
        if vs:
            st.session_state.multi_rag = create_rag_chain(vs, "Citizen")
        else:
            st.session_state.multi_rag = None
    else:
        st.session_state.multi_rag = None

if not st.session_state.multi_rag:
    st.warning("⚠️ Knowledge base not loaded. Run `build_index.py` first.")
    st.stop()

if "multi_messages" not in st.session_state:
    st.session_state.multi_messages = []

# ── Example questions ──────────────────────────────────────────────────────────
if not st.session_state.multi_messages:
    st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.75rem">Example questions</p>', unsafe_allow_html=True)
    examples = [
        ("🇬🇧", "What is the punishment for theft in Pakistan?"),
        ("🇵🇰", "پاکستان میں طلاق کا قانون کیا ہے؟"),
        ("🗣️", "Bail kaise milti hai Pakistan mein?"),
        ("🇬🇧", "What are my rights if police arrests me?"),
        ("🇵🇰", "سائبر کرائم کی سزا کیا ہے؟"),
        ("🗣️", "FIR kaise darj karein?"),
    ]
    cols = st.columns(3)
    for i, (flag, q) in enumerate(examples):
        with cols[i % 3]:
            if st.button(f"{flag} {q}", key=f"ex_{i}"):
                st.session_state["multi_quick_q"] = q

# ── Display messages ───────────────────────────────────────────────────────────
for msg in st.session_state.multi_messages:
    if msg["role"] == "user":
        lang_label = {"english": "EN", "urdu": "UR", "roman_urdu": "RU"}.get(msg.get("lang", "english"), "EN")
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-avatar msg-avatar-user">👤</div>
            <div class="msg-bubble-user">
                <span class="lang-badge">{lang_label}</span>{msg["content"]}
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        is_urdu = msg.get("output_lang") == "urdu"
        bubble_class = "msg-bubble-urdu" if is_urdu else "msg-bubble-ai"
        lang_label = {"english": "EN", "urdu": "UR", "roman_urdu": "RU"}.get(msg.get("output_lang", "english"), "EN")
        content = msg["content"].replace("\n", "<br>")
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-avatar msg-avatar-ai">⚖️</div>
            <div class="{bubble_class}">
                <span class="lang-badge" style="float:{'left' if is_urdu else 'none'}">{lang_label}</span>
                {'<br>' if is_urdu else ''}{content}
            </div>
        </div>""", unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────────────
user_input = st.session_state.pop("multi_quick_q", None)
chat_in = st.chat_input("Ask in English, اردو, or Roman Urdu...")
if chat_in:
    user_input = chat_in

if user_input:
    detected = detect_language(user_input)
    english_q = translate_to_english(user_input) if detected != "english" else user_input

    st.session_state.multi_messages.append({
        "role": "user", "content": user_input, "lang": detected
    })

    with st.spinner("Processing your query..."):
        result = st.session_state.multi_rag.ask(english_q)
        answer_en = result["answer"]

        out_lang = selected_output_lang if selected_output_lang != "auto" else detected

        if out_lang == "urdu":
            answer = translate_to_urdu(answer_en)
        elif out_lang == "roman_urdu":
            answer = translate_to_roman_urdu(answer_en)
        else:
            answer = answer_en

    st.session_state.multi_messages.append({
        "role": "assistant", "content": answer, "output_lang": out_lang
    })
    st.rerun()
