"""
Page 5: Legal Education Mode
MCQs, concept explainer, case scenarios for law students.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agents.legal_education import (
    generate_mcqs, explain_concept, get_case_scenario, LEGAL_TOPICS
)

st.set_page_config(page_title="Legal Education — Mizan", page_icon="📚", layout="wide")

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

.mcq-card {
    background: #0D1017; border: 1px solid #1E2530; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;
}
.mcq-q { font-size: 0.92rem; color: #C8CDD8; font-weight: 500; margin-bottom: 1rem; line-height: 1.5; }
.mcq-num { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #3D4A5C; margin-bottom: 0.4rem; }
.opt-btn { margin: 0.2rem 0; }

.opt-correct {
    background: #0C1F14 !important; border: 1px solid #2D6A4F !important;
    border-radius: 8px !important; padding: 0.6rem 1rem !important;
    color: #4CAF7D !important; width: 100%; text-align: left; font-size: 0.85rem;
    font-family: 'DM Sans', sans-serif; cursor: default;
}
.opt-wrong {
    background: #1A0808 !important; border: 1px solid #5C1A1A !important;
    border-radius: 8px !important; padding: 0.6rem 1rem !important;
    color: #CF6679 !important; width: 100%; text-align: left; font-size: 0.85rem;
    font-family: 'DM Sans', sans-serif; cursor: default;
}
.opt-neutral {
    background: #111620; border: 1px solid #1E2530; border-radius: 8px;
    padding: 0.6rem 1rem; color: #8A95A8; width: 100%; text-align: left;
    font-size: 0.85rem; font-family: 'DM Sans', sans-serif; cursor: default;
}

.explanation-box {
    background: #0A1A0F; border: 1px solid #1A3828; border-radius: 8px;
    padding: 0.8rem 1rem; font-size: 0.8rem; color: #4CAF7D;
    margin-top: 0.75rem; line-height: 1.6;
}

.score-box {
    background: linear-gradient(135deg, #0C1F14, #0A1A0F);
    border: 1px solid #2D6A4F; border-radius: 12px;
    padding: 1.5rem; text-align: center; margin-bottom: 1.5rem;
}
.score-num { font-family: 'DM Mono', monospace; font-size: 3rem; color: #4CAF7D; }
.score-label { font-size: 0.75rem; color: #5A6478; letter-spacing: 0.1em; text-transform: uppercase; }

.concept-box {
    background: #0C1310; border: 1px solid #1A2E1E; border-radius: 12px;
    padding: 1.5rem; font-size: 0.88rem; line-height: 1.9; color: #D4DCC8;
}

.scenario-card {
    background: #0D1017; border: 1px solid #2A3650; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
}
.scenario-label { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #3D4A5C; margin-bottom: 0.4rem; font-weight: 600; }
.difficulty-easy   { color: #4CAF7D; }
.difficulty-medium { color: #C9A84C; }
.difficulty-hard   { color: #CF6679; }

.stButton > button {
    background: linear-gradient(135deg, #1A2235, #111827) !important;
    color: #C9A84C !important; border: 1px solid #2A3650 !important;
    border-radius: 8px !important; font-size: 0.82rem !important; font-weight: 500 !important;
}
.stButton > button:hover { border-color: #C9A84C88 !important; }
.stSelectbox > div > div { background: #111620 !important; border: 1px solid #1E2530 !important; border-radius: 8px !important; }
.stTextInput > div > div > input { background: #111620 !important; border: 1px solid #1E2530 !important; border-radius: 8px !important; color: #C8CDD8 !important; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #1E2530; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-eyebrow">📚 &nbsp; Module 6 · Phase 3</div>
<div class="page-title">Legal <em>Education</em></div>
<div class="page-sub">MCQ Practice · Concept Explainer · Case Scenarios — for LLB students and bar exam prep</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 MCQ Quiz", "💡 Concept Explainer", "📋 Case Scenarios"])

# ── Tab 1: MCQ Quiz ────────────────────────────────────────────────────────────
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        topic = st.selectbox("Subject", list(LEGAL_TOPICS.keys()))
    with col2:
        subtopics = LEGAL_TOPICS.get(topic, ["General"])
        subtopic = st.selectbox("Topic", subtopics)
    with col3:
        num_q = st.selectbox("Questions", [5, 10, 15], index=0)

    if st.button("▶  Start Quiz", use_container_width=False):
        with st.spinner("Generating questions..."):
            questions = generate_mcqs(topic, subtopic, num_q)
        st.session_state["quiz_questions"] = questions
        st.session_state["quiz_answers"] = {}
        st.session_state["quiz_submitted"] = False
        st.session_state["quiz_topic"] = f"{topic} — {subtopic}"

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "quiz_questions" in st.session_state and st.session_state["quiz_questions"]:
        questions = st.session_state["quiz_questions"]
        submitted = st.session_state.get("quiz_submitted", False)

        if submitted:
            correct = sum(
                1 for i, q in enumerate(questions)
                if st.session_state["quiz_answers"].get(i) == q.get("correct")
            )
            pct = int(correct / len(questions) * 100)
            grade = "Excellent" if pct >= 80 else "Good" if pct >= 60 else "Needs Practice"
            st.markdown(f"""
            <div class="score-box">
                <div class="score-num">{correct}/{len(questions)}</div>
                <div class="score-label">{pct}% · {grade}</div>
            </div>""", unsafe_allow_html=True)

        for i, q in enumerate(questions):
            user_ans = st.session_state["quiz_answers"].get(i)
            correct_ans = q.get("correct", "A")

            st.markdown(f"""
            <div class="mcq-card">
                <div class="mcq-num">Q{i+1} of {len(questions)} &nbsp;·&nbsp; {st.session_state.get('quiz_topic','')}</div>
                <div class="mcq-q">{q.get('question', '')}</div>
            """, unsafe_allow_html=True)

            for opt_key, opt_text in q.get("options", {}).items():
                label = f"{opt_key}.  {opt_text}"
                if submitted:
                    if opt_key == correct_ans:
                        st.markdown(f'<div class="opt-correct">✓ {label}</div>', unsafe_allow_html=True)
                    elif opt_key == user_ans:
                        st.markdown(f'<div class="opt-wrong">✗ {label}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="opt-neutral">{label}</div>', unsafe_allow_html=True)
                else:
                    is_selected = user_ans == opt_key
                    btn_style = "border-color: #C9A84C !important; color: #C9A84C !important;" if is_selected else ""
                    if st.button(label, key=f"opt_{i}_{opt_key}"):
                        st.session_state["quiz_answers"][i] = opt_key
                        st.rerun()

            if submitted and q.get("explanation"):
                st.markdown(f'<div class="explanation-box">💡 {q["explanation"]}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if not submitted:
                answered = len(st.session_state["quiz_answers"])
                if st.button(f"✓  Submit Quiz ({answered}/{len(questions)} answered)"):
                    st.session_state["quiz_submitted"] = True
                    st.rerun()
        with col_b:
            if submitted:
                if st.button("↺  New Quiz"):
                    for key in ["quiz_questions", "quiz_answers", "quiz_submitted", "quiz_topic"]:
                        st.session_state.pop(key, None)
                    st.rerun()

# ── Tab 2: Concept Explainer ───────────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns([2, 1])
    with col1:
        concept = st.text_input(
            "Enter a legal concept",
            placeholder="e.g. Qisas, Diyat, Habeas Corpus, Mens Rea, Estoppel, Khula...",
            label_visibility="collapsed",
        )
    with col2:
        level = st.selectbox("Level", ["beginner", "student", "professional"])

    if st.button("💡  Explain Concept") and concept.strip():
        with st.spinner(f"Explaining '{concept}'..."):
            explanation = explain_concept(concept, level)
        st.session_state["concept_result"] = explanation
        st.session_state["concept_name"] = concept

    if "concept_result" in st.session_state:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.5rem">{st.session_state.get("concept_name","")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="concept-box">{st.session_state["concept_result"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇ Download Explanation",
            data=st.session_state["concept_result"],
            file_name=f"{st.session_state.get('concept_name','concept')}_explanation.txt",
            mime="text/plain",
        )

# ── Tab 3: Case Scenarios ──────────────────────────────────────────────────────
with tab3:
    st.markdown('<p style="font-size:0.78rem;color:#5A6478;margin-bottom:1rem">Practice with realistic Pakistani legal scenarios. Read the case and think of your answer before revealing the model answer.</p>', unsafe_allow_html=True)

    scenario_topic = st.selectbox("Choose Topic for Scenario", list(LEGAL_TOPICS.keys()), key="sc_topic")

    if st.button("🎲  Generate Scenario"):
        with st.spinner("Generating case scenario..."):
            scenario = get_case_scenario(scenario_topic)
        st.session_state["scenario"] = scenario
        st.session_state["show_answer"] = False

    if "scenario" in st.session_state:
        sc = st.session_state["scenario"]
        diff = sc.get("difficulty", "Medium")
        diff_class = {"Easy": "difficulty-easy", "Medium": "difficulty-medium", "Hard": "difficulty-hard"}.get(diff, "difficulty-medium")

        st.markdown(f"""
        <div class="scenario-card">
            <div class="scenario-label">Case Scenario &nbsp;·&nbsp; <span class="{diff_class}">{diff}</span></div>
            <div style="font-size:0.92rem;color:#C8CDD8;line-height:1.7;margin-bottom:1rem">{sc.get('scenario','')}</div>
            <div style="font-size:0.88rem;color:#C9A84C;font-weight:500">❓ {sc.get('question','')}</div>
        </div>""", unsafe_allow_html=True)

        if sc.get("key_issues"):
            st.markdown('<div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.4rem">Key Issues</div>', unsafe_allow_html=True)
            issues_html = " &nbsp;·&nbsp; ".join(f'<span style="color:#7A8BA0;font-size:0.78rem">{i}</span>' for i in sc["key_issues"])
            st.markdown(issues_html, unsafe_allow_html=True)

        if sc.get("applicable_laws"):
            st.markdown('<div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-top:0.75rem;margin-bottom:0.4rem">Applicable Laws</div>', unsafe_allow_html=True)
            laws_html = " &nbsp; ".join(f'<span style="background:#1A1A08;border:1px solid #2A2A18;border-radius:5px;padding:0.15rem 0.5rem;font-size:0.72rem;color:#C9A84C">{l}</span>' for l in sc["applicable_laws"])
            st.markdown(laws_html, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁  Reveal Model Answer"):
                st.session_state["show_answer"] = True
        with col2:
            if st.button("🎲  New Scenario"):
                st.session_state.pop("scenario", None)
                st.session_state.pop("show_answer", None)
                st.rerun()

        if st.session_state.get("show_answer"):
            st.markdown(f'<div class="concept-box">{sc.get("model_answer","").replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
