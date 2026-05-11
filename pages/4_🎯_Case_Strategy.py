"""
Page 4: Case Strategy Agent + Court Procedure Guide
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agents.case_strategy import get_case_strategy, get_court_procedure, PROCEDURE_LIST

st.set_page_config(page_title="Case Strategy — Mizan", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap');
html, body, .stApp { background: #0A0C0F !important; color: #E8E4DC !important; font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1100px !important; }

.page-eyebrow { font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.5rem; }
.page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 300; color: #E8E4DC; line-height: 1.1; margin-bottom: 0.4rem; }
.page-title em { font-style: italic; color: #C9A84C; }
.page-sub { font-size: 0.85rem; color: #5A6478; margin-bottom: 2rem; }

.stTextArea textarea {
    background: #111620 !important; border: 1px solid #1E2530 !important;
    border-radius: 8px !important; color: #C8CDD8 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important;
}
.stTextArea label, .stSelectbox label, .stRadio label {
    color: #5A6478 !important; font-size: 0.75rem !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
}
.stSelectbox > div > div { background: #111620 !important; border: 1px solid #1E2530 !important; border-radius: 8px !important; }

.stButton > button {
    background: linear-gradient(135deg, #C9A84C22, #C9A84C11) !important;
    color: #C9A84C !important; border: 1px solid #C9A84C55 !important;
    border-radius: 8px !important; font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.7rem 2rem !important;
}
.stButton > button:hover { border-color: #C9A84C !important; }

.output-box {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 12px;
    padding: 1.5rem 2rem; font-size: 0.88rem; line-height: 1.9; color: #D4DCC8;
    max-height: 650px; overflow-y: auto;
}

.proc-card {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 10px;
    padding: 1rem; text-align: center; cursor: pointer; margin-bottom: 0.5rem;
}
.proc-card:hover { border-color: #C9A84C44; background: #111620; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }

.disclaimer {
    background: #0D1017; border: 1px solid #1E2530; border-left: 3px solid #C9A84C44;
    border-radius: 8px; padding: 0.8rem 1.1rem; font-size: 0.75rem; color: #3D4A5C;
    margin-top: 1.5rem; line-height: 1.6;
}
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #1E2530; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-eyebrow">🎯 &nbsp; Module 5 · Phase 3</div>
<div class="page-title">Case Strategy <em>Agent</em></div>
<div class="page-sub">Describe your legal situation — AI builds a complete strategy and roadmap</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚖️ Case Strategy", "🏛️ Court Procedure Guide"])

# ── Tab 1: Case Strategy ───────────────────────────────────────────────────────
with tab1:
    st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:1rem;font-weight:600">Describe Your Situation</p>', unsafe_allow_html=True)

    situation = st.text_area(
        "What happened? Describe your legal situation in detail.",
        height=150,
        placeholder="e.g. My employer fired me without notice after 5 years of service and refused to pay my dues. I have no written employment contract but have salary slips and bank statements showing payments...",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        role = st.selectbox("Your Role", ["Complainant", "Accused", "Victim", "Employer", "Employee", "Landlord", "Tenant", "Other"])
    with col2:
        urgency = st.selectbox("Urgency", ["Urgent (within days)", "Soon (within weeks)", "Not immediate"])
    with col3:
        resources = st.selectbox("Resources", ["Can afford a lawyer", "Limited budget", "Need free legal aid", "Self-representation"])

    if st.button("⚖️  Generate Legal Strategy", use_container_width=False):
        if not situation.strip() or len(situation.strip()) < 30:
            st.warning("Please describe your situation in more detail (at least 30 characters).")
        else:
            with st.spinner("Building your legal strategy..."):
                strategy = get_case_strategy(situation, role, urgency, resources)
            st.session_state["strategy_result"] = strategy

    if "strategy_result" in st.session_state:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state["strategy_result"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇ Download Strategy",
            data=st.session_state["strategy_result"],
            file_name="legal_strategy.txt",
            mime="text/plain",
        )
        st.markdown("""
        <div class="disclaimer">
            <strong style="color:#C9A84C88">Disclaimer</strong> &nbsp;·&nbsp;
            This strategy is AI-generated for informational purposes only. It is not legal advice.
            Always consult a qualified Pakistani lawyer before taking legal action.
        </div>""", unsafe_allow_html=True)

# ── Tab 2: Court Procedure Guide ───────────────────────────────────────────────
with tab2:
    st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:1rem;font-weight:600">Select a Procedure</p>', unsafe_allow_html=True)

    proc_icons = {
        "File an FIR": "🚔",
        "Apply for Bail": "🔓",
        "File a Civil Suit": "📋",
        "Appeal a Judgment": "⚖️",
        "File Khula/Divorce": "💍",
        "Consumer Complaint": "🛒",
        "Labour Complaint": "👷",
        "Cybercrime Complaint": "💻",
    }

    cols = st.columns(4)
    for i, proc in enumerate(PROCEDURE_LIST):
        with cols[i % 4]:
            icon = proc_icons.get(proc, "📄")
            if st.button(f"{icon}\n{proc}", key=f"proc_{proc}", use_container_width=True):
                st.session_state["selected_proc"] = proc

    if "selected_proc" in st.session_state:
        proc = st.session_state["selected_proc"]
        st.markdown(f'<div style="font-size:0.85rem;color:#C9A84C;margin:1rem 0 0.5rem">{proc_icons.get(proc,"📄")} {proc}</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if f"proc_result_{proc}" not in st.session_state:
            with st.spinner(f"Loading {proc} guide..."):
                st.session_state[f"proc_result_{proc}"] = get_court_procedure(proc)

        result = st.session_state[f"proc_result_{proc}"]
        st.markdown(f'<div class="output-box">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button(
            f"⬇ Download {proc} Guide",
            data=result,
            file_name=f"{proc.replace(' ', '_')}_guide.txt",
            mime="text/plain",
        )
