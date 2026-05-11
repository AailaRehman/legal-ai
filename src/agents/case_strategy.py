"""
Case Strategy Agent
Analyzes a legal situation and suggests strategy, steps, and relevant laws.
"""

import os
from pathlib import Path
from typing import Dict, Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


def get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0.2, max_tokens=3000)


STRATEGY_PROMPT = """You are a senior Pakistani legal strategist with 25 years of courtroom experience.

A client has described their legal situation. Provide a comprehensive legal strategy.

SITUATION:
{situation}

Role of Client: {role} (Complainant/Accused/Victim/Witness/Other)
Urgency: {urgency}
Resources Available: {resources}

Provide your strategy in this EXACT format:

## ⚖️ Legal Assessment
[Assess the strength of the case. Be honest about chances.]

## 📋 Applicable Laws & Sections
[List every relevant Pakistani law, section, and article with brief explanation]

## 🎯 Recommended Legal Strategy
[Step-by-step strategic approach. What to do first, second, third.]

## ⚡ Immediate Actions (Next 48-72 hours)
[What must be done urgently]

## 📅 Step-by-Step Legal Process
[Complete roadmap from current situation to resolution]

## 💪 Strengths of Your Position
[What works in the client's favor]

## ⚠️ Weaknesses & Risks
[Honest assessment of risks and weaknesses]

## 🏛️ Which Court / Forum
[Exactly which court, tribunal, or authority to approach]

## 📄 Documents Required
[Complete list of documents to gather immediately]

## 💰 Estimated Timeline & Costs
[Realistic timeline and approximate legal costs in Pakistan]

## ❌ What NOT To Do
[Common mistakes to avoid in this type of case]

---
⚠️ This is AI-generated legal strategy for educational purposes only.
Consult a qualified Pakistani lawyer before taking any legal action.
"""


PROCEDURE_PROMPTS = {
    "File an FIR": """Explain the complete step-by-step process to file an FIR in Pakistan.
Include: which police station, what to bring, what to say, what if police refuses,
legal rights during FIR filing, Section 154 CrPC, remedies if FIR is refused.
Be very specific and practical.""",

    "Apply for Bail": """Explain the complete bail process in Pakistan.
Include: types of bail (pre-arrest, post-arrest, transit), which court,
documents needed, Section 496-499 CrPC, grounds for bail,
what happens at bail hearing, surety requirements, bail bonds.
Be very specific and practical.""",

    "File a Civil Suit": """Explain how to file a civil suit in Pakistani courts.
Include: which court (District Court, High Court), court fees,
plaint requirements, limitation period, summons process,
evidence filing, trial procedure, appeal process.
Be very specific and practical.""",

    "Appeal a Judgment": """Explain how to appeal a court judgment in Pakistan.
Include: appeal hierarchy (Sessions → High Court → Supreme Court),
limitation periods for appeal, grounds for appeal,
stay of execution, documents needed, appeal process.
Be very specific and practical.""",

    "File Khula/Divorce": """Explain the complete Khula and divorce process in Pakistan.
Include: Family Court jurisdiction, required documents,
Khula vs Talaq vs Judicial Divorce differences,
maintenance rights, child custody, iddat period,
timeline and what to expect at each hearing.
Be very specific and practical.""",

    "Consumer Complaint": """Explain how to file a consumer complaint in Pakistan.
Include: Consumer Protection Councils, which forum,
online complaint process, documents needed,
Punjab Consumer Protection Act, remedies available,
timeline for resolution. Be very specific.""",

    "Labour Complaint": """Explain how to file a labour/employment complaint in Pakistan.
Include: Labour Court, NIRC, which forum for which issue,
wrongful termination, wage theft, EOBI, PESSI,
Industrial Relations Act 2012, timeline and remedies.""",

    "Cybercrime Complaint": """Explain how to report cybercrime in Pakistan under PECA 2016.
Include: FIA Cybercrime Wing, online complaint portal,
what evidence to preserve, Section-wise offences,
process after complaint, investigation timeline,
what to do if harassed online. Be very practical.""",
}


def get_case_strategy(situation: str, role: str, urgency: str, resources: str) -> str:
    """Generate a comprehensive legal strategy for a given situation."""
    llm = get_llm()
    prompt = STRATEGY_PROMPT.format(
        situation=situation,
        role=role,
        urgency=urgency,
        resources=resources,
    )
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


def get_court_procedure(procedure_name: str) -> str:
    """Get step-by-step guide for a specific court procedure."""
    llm = get_llm()
    base_prompt = PROCEDURE_PROMPTS.get(procedure_name, f"Explain the process for: {procedure_name}")

    system = """You are an expert Pakistani legal procedure guide.
Give practical, step-by-step instructions that a common person can follow.
Use numbered steps. Include specific laws, sections, forms, fees, and timeframes.
Always end with: '⚠️ Consult a qualified lawyer for your specific situation.'"""

    response = llm.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": base_prompt}
    ])
    return response.content


PROCEDURE_LIST = list(PROCEDURE_PROMPTS.keys())
