"""
Page 1: Legal Document Analyzer
Upload any legal document → AI analyzes it instantly.
"""

import sys
import os
import tempfile
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.document_analyzer import analyze_document, score_document_risk, extract_entities
from src.ingestion.document_loader import load_document

st.set_page_config(page_title="Document Analyzer — Mizan", page_icon="📄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap');

html, body, .stApp { background: #0A0C0F !important; color: #E8E4DC !important; font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1200px !important; }

.page-header { margin-bottom: 2rem; }
.page-eyebrow { font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.5rem; }
.page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 300; color: #E8E4DC; line-height: 1.1; }
.page-title em { font-style: italic; color: #C9A84C; }
.page-sub { font-size: 0.85rem; color: #5A6478; margin-top: 0.4rem; }

.upload-zone {
    border: 1px dashed #2A3650; border-radius: 12px;
    background: #0D1017; padding: 2rem;
    text-align: center; margin-bottom: 1.5rem;
}
.upload-zone p { color: #5A6478; font-size: 0.85rem; margin-top: 0.5rem; }

.risk-card {
    border-radius: 12px; padding: 1.5rem;
    border: 1px solid; margin-bottom: 1.5rem;
}
.risk-low    { background: #0C1F14; border-color: #1A3828; }
.risk-medium { background: #1A1A08; border-color: #3D3D0A; }
.risk-high   { background: #1A0C08; border-color: #3D1A0A; }
.risk-critical { background: #1A0808; border-color: #3D0A0A; }

.risk-score-num { font-family: 'DM Mono', monospace; font-size: 3rem; font-weight: 500; line-height: 1; }
.risk-low .risk-score-num    { color: #4CAF7D; }
.risk-medium .risk-score-num { color: #C9A84C; }
.risk-high .risk-score-num   { color: #CF8A4A; }
.risk-critical .risk-score-num { color: #CF6679; }

.risk-label { font-size: 0.75rem; letter-spacing: 0.15em; text-transform: uppercase; color: #5A6478; margin-top: 0.25rem; }
.risk-factors { margin-top: 1rem; }
.risk-factor-item { font-size: 0.8rem; color: #8A95A8; padding: 0.3rem 0; border-bottom: 1px solid #1E2530; }

.entity-section { margin-bottom: 1.5rem; }
.entity-label { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #3D4A5C; margin-bottom: 0.5rem; font-weight: 600; }
.entity-chip {
    display: inline-block; background: #111620; border: 1px solid #1E2A30;
    border-radius: 6px; padding: 0.2rem 0.6rem; font-size: 0.75rem;
    color: #7A8BA0; margin: 0.2rem; font-family: 'DM Mono', monospace;
}
.entity-chip.law { color: #C9A84C; border-color: #2A2A18; background: #1A1A08; }
.entity-chip.person { color: #4CAF7D; border-color: #1A2A1E; background: #0C1810; }
.entity-chip.date { color: #7A8ACF; border-color: #1A1A2A; background: #0C0C18; }
.entity-chip.amount { color: #CF8A4A; border-color: #2A1A0A; background: #180C08; }

.analysis-box {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 12px;
    padding: 1.5rem; font-size: 0.88rem; line-height: 1.8; color: #C8D4C0;
}
.analysis-box h2 { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: #C9A84C; margin: 1rem 0 0.4rem; }
.analysis-box h3 { font-size: 0.8rem; color: #5A6478; letter-spacing: 0.1em; text-transform: uppercase; margin: 0.75rem 0 0.25rem; }
.analysis-box ul { padding-left: 1.2rem; }
.analysis-box li { margin: 0.25rem 0; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }

.stButton > button {
    background: linear-gradient(135deg, #1A2235, #111827) !important;
    color: #C9A84C !important; border: 1px solid #2A3650 !important;
    border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important; font-weight: 500 !important; padding: 0.6rem 1.5rem !important;
}
.stButton > button:hover { border-color: #C9A84C88 !important; color: #E8C96A !important; }

[data-testid="stTab"] { font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">📄 &nbsp; Module 2 · Phase 2</div>
    <div class="page-title">Document <em>Analyzer</em></div>
    <div class="page-sub">Upload any legal document — FIR, contract, notice, court order — and get instant AI analysis</div>
</div>
""", unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload legal document",
    type=["pdf", "txt"],
    label_visibility="collapsed",
    help="Supports: FIR, Contracts, Notices, Court Orders, Agreements, Affidavits"
)

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    with st.spinner("Reading document..."):
        try:
            doc_text = load_document(tmp_path)
            os.unlink(tmp_path)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            st.stop()

    if not doc_text or len(doc_text) < 50:
        st.error("Document appears to be empty or unreadable. Try a different file.")
        st.stop()

    st.markdown(f'<div style="font-size:0.78rem;color:#3D4A5C;margin-bottom:1rem">📄 {uploaded.name} &nbsp;·&nbsp; {len(doc_text):,} characters extracted</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["⚖️ Full Analysis", "🔴 Risk Score", "🔍 Entities", "📄 Raw Text"])

    # Tab 1: Full Analysis
    with tab1:
        with st.spinner("Analyzing document with AI..."):
            result = analyze_document(doc_text)
        analysis_html = result["analysis"].replace("\n", "<br>").replace("##", "<h2>").replace("#", "<h3>")
        st.markdown(f'<div class="analysis-box">{result["analysis"]}</div>', unsafe_allow_html=True)

        st.download_button(
            "⬇ Download Analysis",
            data=result["analysis"],
            file_name=f"analysis_{uploaded.name}.txt",
            mime="text/plain",
        )

    # Tab 2: Risk Score
    with tab2:
        with st.spinner("Calculating risk score..."):
            risk = score_document_risk(doc_text)

        score = risk.get("risk_score", 50)
        level = risk.get("risk_level", "Unknown")
        risk_class = {
            "Low": "risk-low", "Medium": "risk-medium",
            "High": "risk-high", "Critical": "risk-critical"
        }.get(level, "risk-medium")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class="risk-card {risk_class}">
                <div class="risk-score-num">{score}</div>
                <div class="risk-label">Risk Score / 100</div>
                <div style="margin-top:0.75rem;font-size:1rem;font-weight:600;color:#E8E4DC">{level} Risk</div>
                <div style="margin-top:0.4rem;font-size:0.78rem;color:#5A6478">
                    Document Type: {risk.get('document_type', 'Unknown')}
                </div>
                {"<div style='margin-top:0.75rem;background:#3D0A0A;border-radius:6px;padding:0.4rem 0.6rem;font-size:0.75rem;color:#CF6679'>⚠️ Urgent Action Required</div>" if risk.get('urgent_action_required') else ""}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if risk.get("risk_factors"):
                st.markdown('<div class="entity-label">⚠️ Risk Factors</div>', unsafe_allow_html=True)
                for f in risk["risk_factors"]:
                    st.markdown(f'<div class="risk-factor-item">⚠ {f}</div>', unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)

            if risk.get("missing_clauses"):
                st.markdown('<div class="entity-label">❌ Missing Clauses</div>', unsafe_allow_html=True)
                for c in risk["missing_clauses"]:
                    st.markdown(f'<div class="risk-factor-item" style="color:#CF6679">✗ {c}</div>', unsafe_allow_html=True)

            if risk.get("positive_points"):
                st.markdown('<div class="entity-label" style="margin-top:1rem">✅ Positive Points</div>', unsafe_allow_html=True)
                for p in risk["positive_points"]:
                    st.markdown(f'<div class="risk-factor-item" style="color:#4CAF7D">✓ {p}</div>', unsafe_allow_html=True)

    # Tab 3: Entity Extraction
    with tab3:
        with st.spinner("Extracting legal entities..."):
            entities = extract_entities(doc_text)

        def render_chips(items, chip_class=""):
            if not items:
                return '<span style="color:#3D4A5C;font-size:0.78rem">None found</span>'
            return "".join(f'<span class="entity-chip {chip_class}">{i}</span>' for i in items)

        cols = st.columns(2)
        with cols[0]:
            st.markdown('<div class="entity-label">👥 Persons</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("persons", []), "person"), unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)

            st.markdown('<div class="entity-label">📅 Dates</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("dates", []), "date"), unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)

            st.markdown('<div class="entity-label">💰 Amounts</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("amounts", []), "amount"), unsafe_allow_html=True)

        with cols[1]:
            st.markdown('<div class="entity-label">⚖️ Law Sections</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("law_sections", []), "law"), unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)

            st.markdown('<div class="entity-label">🏢 Organizations</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("organizations", []), ""), unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)

            st.markdown('<div class="entity-label">📍 Locations</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("locations", []), ""), unsafe_allow_html=True)

        if entities.get("case_numbers"):
            st.markdown('<br><div class="entity-label">📋 Case Numbers</div>', unsafe_allow_html=True)
            st.markdown(render_chips(entities.get("case_numbers", []), ""), unsafe_allow_html=True)

    # Tab 4: Raw Text
    with tab4:
        st.markdown(f'<div style="background:#0D1017;border:1px solid #1E2530;border-radius:8px;padding:1rem;font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#5A6478;white-space:pre-wrap;max-height:500px;overflow-y:auto">{doc_text[:5000]}{"..." if len(doc_text) > 5000 else ""}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="upload-zone">
        <div style="font-size:2rem">📄</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#8A95A8;margin-top:0.5rem">Drop your legal document here</div>
        <p>Supports: FIR · Contract · Notice · Court Order · Agreement · Affidavit · PDF or TXT</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **What this analyzer detects:**

    | Feature | Description |
    |---|---|
    | 📋 Document Type | Auto-identifies FIR, Contract, Notice, etc. |
    | ⚠️ Risk Score | 0–100 risk rating with specific risk factors |
    | ❌ Missing Clauses | Identifies legally required clauses that are absent |
    | 👥 Entity Extraction | Persons, organizations, dates, amounts, law sections |
    | ⚖️ Applicable Laws | Relevant Pakistani laws and sections |
    | 💡 Recommendations | Specific actions to take |
    """)
