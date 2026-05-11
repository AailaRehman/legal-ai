"""
Legal Document Analyzer
Summarizes, detects risks, extracts clauses from uploaded legal docs.
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain.schema import Document
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


def get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0.1, max_tokens=3000)


ANALYZER_PROMPT = """You are an expert Pakistani legal document analyst.

Analyze the following legal document and provide a structured analysis in this EXACT format:

## 📋 Document Type
[Identify: FIR / Contract / Notice / Court Order / Agreement / Affidavit / Other]

## 📝 Summary
[2-3 sentence plain English summary of what this document is about]

## 👥 Parties Involved
[List all parties mentioned with their roles]

## ⚠️ Key Risks & Red Flags
[List any risky clauses, missing protections, or legal concerns. Be specific.]

## ✅ Key Clauses & Rights
[List important clauses, rights, or obligations found in the document]

## 📅 Important Dates & Deadlines
[Any dates, deadlines, or time-sensitive information]

## 🔍 Legal Issues Detected
[Any violations of Pakistani law, missing required elements, or legal problems]

## 💡 Recommendations
[What should the person do? Any urgent actions needed?]

## ⚖️ Applicable Laws
[Which Pakistani laws, sections, or acts apply to this document]

---
DOCUMENT TO ANALYZE:
{document_text}

Provide thorough, accurate analysis. If this is a contract, focus on risk detection.
If this is an FIR, check for legal compliance. Always cite relevant Pakistani laws.
End with: "⚠️ Consult a qualified lawyer before taking any legal action."
"""

RISK_SCORING_PROMPT = """You are a Pakistani legal risk assessment expert.

Analyze this document and provide ONLY a JSON response in this exact format:
{{
    "risk_score": <number 0-100>,
    "risk_level": "<Low/Medium/High/Critical>",
    "risk_factors": ["<factor1>", "<factor2>", "<factor3>"],
    "missing_clauses": ["<clause1>", "<clause2>"],
    "positive_points": ["<point1>", "<point2>"],
    "urgent_action_required": <true/false>,
    "document_type": "<type>"
}}

Document:
{document_text}

Return ONLY valid JSON, no other text."""


def analyze_document(text: str) -> Dict[str, Any]:
    """Full document analysis — summary, risks, clauses, recommendations."""
    llm = get_llm()
    prompt = ANALYZER_PROMPT.format(document_text=text[:6000])
    response = llm.invoke([{"role": "user", "content": prompt}])
    return {"analysis": response.content}


def score_document_risk(text: str) -> Dict[str, Any]:
    """Risk scoring — returns structured JSON risk assessment."""
    import json
    llm = get_llm()
    prompt = RISK_SCORING_PROMPT.format(document_text=text[:4000])
    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        raw = response.content.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception:
        return {
            "risk_score": 50,
            "risk_level": "Unknown",
            "risk_factors": ["Could not parse risk assessment"],
            "missing_clauses": [],
            "positive_points": [],
            "urgent_action_required": False,
            "document_type": "Unknown"
        }


def extract_entities(text: str) -> Dict[str, Any]:
    """Extract key legal entities — names, dates, amounts, sections."""
    llm = get_llm()
    prompt = f"""Extract key legal entities from this Pakistani legal document.
Return ONLY JSON in this format:
{{
    "persons": ["<name1>", "<name2>"],
    "organizations": ["<org1>"],
    "dates": ["<date1>", "<date2>"],
    "amounts": ["<amount1>"],
    "locations": ["<loc1>"],
    "law_sections": ["<Section X PPC>", "<Article Y Constitution>"],
    "case_numbers": ["<case no>"]
}}

Document:
{text[:3000]}

Return ONLY valid JSON."""

    import json
    response = llm.invoke([{"role": "user", "content": prompt}])
    try:
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception:
        return {"persons": [], "organizations": [], "dates": [],
                "amounts": [], "locations": [], "law_sections": [], "case_numbers": []}
