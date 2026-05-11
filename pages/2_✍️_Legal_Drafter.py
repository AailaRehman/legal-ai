"""
Page 2: Legal Document Drafter
Generate professional Pakistani legal documents with AI.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.legal_drafter import draft_document, get_document_fields, TEMPLATES

st.set_page_config(page_title="Legal Drafter — Mizan", page_icon="✍️", layout="wide")

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

.doc-type-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-bottom: 2rem; }
.doc-type-card {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 10px;
    padding: 1rem; text-align: center; cursor: pointer; transition: all 0.2s;
}
.doc-type-card:hover { border-color: #C9A84C44; background: #111620; }
.doc-type-card.active { border-color: #C9A84C; background: #111620; }
.doc-type-icon { font-size: 1.4rem; margin-bottom: 0.35rem; }
.doc-type-name { font-size: 0.78rem; color: #8A95A8; font-weight: 500; }

.form-section {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 12px;
    padding: 1.5rem; margin-bottom: 1.5rem;
}
.form-section-title {
    font-family: 'Cormorant Garamond', serif; font-size: 1.2rem;
    color: #C9A84C; margin-bottom: 1rem;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #111620 !important; border: 1px solid #1E2530 !important;
    border-radius: 8px !important; color: #C8CDD8 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: #5A6478 !important; font-size: 0.78rem !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
}

.stButton > button {
    background: linear-gradient(135deg, #C9A84C22, #C9A84C11) !important;
    color: #C9A84C !important; border: 1px solid #C9A84C55 !important;
    border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important; font-weight: 600 !important;
    padding: 0.7rem 2rem !important; letter-spacing: 0.05em !important;
}
.stButton > button:hover { border-color: #C9A84C !important; background: linear-gradient(135deg, #C9A84C33, #C9A84C22) !important; }

.output-box {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 12px;
    padding: 1.5rem 2rem; font-size: 0.88rem; line-height: 1.9;
    color: #D4DCC8; font-family: 'DM Mono', monospace; white-space: pre-wrap;
    max-height: 600px; overflow-y: auto;
}

.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0A0C0F; }
::-webkit-scrollbar-thumb { background: #1E2530; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">✍️ &nbsp; Module 3 · Phase 2</div>
    <div class="page-title">Legal <em>Drafter</em></div>
    <div class="page-sub">Generate professional Pakistani legal documents — ready for advocate review</div>
</div>
""", unsafe_allow_html=True)

# ── Document type selector ─────────────────────────────────────────────────────
doc_icons = {
    "Legal Notice": "📜",
    "Affidavit": "📋",
    "Rent Agreement": "🏠",
    "FIR Draft": "🚔",
    "NDA Agreement": "🤫",
    "Power of Attorney": "✋",
    "Petition": "⚖️",
    "Contract Agreement": "🤝",
}

if "selected_doc_type" not in st.session_state:
    st.session_state.selected_doc_type = "Legal Notice"

st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.75rem;font-weight:600">Select Document Type</p>', unsafe_allow_html=True)

cols = st.columns(4)
for i, (doc_type, icon) in enumerate(doc_icons.items()):
    with cols[i % 4]:
        is_active = st.session_state.selected_doc_type == doc_type
        border = "#C9A84C" if is_active else "#1E2530"
        bg = "#111620" if is_active else "#0D1017"
        name_color = "#C9A84C" if is_active else "#8A95A8"
        if st.button(f"{icon}\n{doc_type}", key=f"dt_{doc_type}"):
            st.session_state.selected_doc_type = doc_type
            st.rerun()

st.markdown(f'<div style="font-size:0.78rem;color:#C9A84C;margin-bottom:1.5rem">Selected: {doc_icons[st.session_state.selected_doc_type]} {st.session_state.selected_doc_type}</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Form fields ────────────────────────────────────────────────────────────────
doc_type = st.session_state.selected_doc_type
fields = get_document_fields(doc_type)

st.markdown(f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.3rem;color:#C9A84C;margin-bottom:1rem">{doc_icons[doc_type]} {doc_type} — Details</div>', unsafe_allow_html=True)

field_values = {}
cols_per_row = 2
field_list = list(fields.items())

for i in range(0, len(field_list), cols_per_row):
    row_fields = field_list[i:i+cols_per_row]
    cols = st.columns(cols_per_row)
    for j, (field_key, field_label) in enumerate(row_fields):
        with cols[j]:
            # Use textarea for long fields
            long_fields = {"issue_description", "facts", "incident_description",
                          "legal_grounds", "relief", "powers", "subject_matter",
                          "obligations_one", "obligations_two", "special_conditions"}
            if field_key in long_fields:
                field_values[field_key] = st.text_area(
                    field_label, height=100, key=f"field_{field_key}",
                    placeholder=f"Enter {field_label.lower()}..."
                )
            else:
                field_values[field_key] = st.text_input(
                    field_label, key=f"field_{field_key}",
                    placeholder=f"Enter {field_label.lower()}..."
                )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Generate button ────────────────────────────────────────────────────────────
if st.button(f"✦  Generate {doc_type}", use_container_width=False):
    empty_required = [label for key, label in fields.items()
                      if not field_values.get(key, "").strip()]

    if len(empty_required) > len(fields) // 2:
        st.warning(f"Please fill in at least half the fields to generate a useful document.")
    else:
        # Fill empty optional fields with placeholder
        for key in field_values:
            if not field_values[key].strip():
                field_values[key] = "[To be specified]"

        with st.spinner(f"Drafting {doc_type}..."):
            document = draft_document(doc_type, field_values)

        st.session_state["generated_doc"] = document
        st.session_state["generated_doc_type"] = doc_type

# ── Output ─────────────────────────────────────────────────────────────────────
if "generated_doc" in st.session_state:
    doc = st.session_state["generated_doc"]
    dtype = st.session_state["generated_doc_type"]

    st.markdown(f'<div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.75rem;font-weight:600">Generated Document</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{doc}</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇ Download as TXT",
            data=doc,
            file_name=f"{dtype.replace(' ', '_')}_draft.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        if st.button("✕  Clear Document", use_container_width=True):
            del st.session_state["generated_doc"]
            del st.session_state["generated_doc_type"]
            st.rerun()

    st.markdown("""
    <div style="background:#0D1017;border:1px solid #1E2530;border-left:3px solid #C9A84C44;
    border-radius:8px;padding:0.8rem 1.1rem;font-size:0.75rem;color:#3D4A5C;margin-top:1rem;line-height:1.6">
        <strong style="color:#C9A84C88">Disclaimer</strong> &nbsp;·&nbsp;
        This is an AI-generated draft for reference only. Have it reviewed and signed by a qualified
        Pakistani lawyer before submission. Some documents may require stamp paper, registration,
        or notarization under Pakistani law.
    </div>
    """, unsafe_allow_html=True)
