"""
Legal Education Module
MCQs, concept explainer, and exam prep for Pakistani law students.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

LEGAL_TOPICS = {
    "Constitution of Pakistan": [
        "Fundamental Rights (Articles 8-28)",
        "Federal Structure & Parliament",
        "Judiciary & Supreme Court",
        "Emergency Provisions",
        "Amendment Procedure",
    ],
    "Pakistan Penal Code (PPC)": [
        "Offences Against Person (302-338)",
        "Offences Against Property (378-420)",
        "Hudood Offences",
        "Defamation & Public Order",
        "Abetment & Conspiracy",
    ],
    "Code of Criminal Procedure (CrPC)": [
        "FIR & Investigation",
        "Bail Provisions",
        "Trial Procedure",
        "Appeals & Revisions",
        "Arrest & Detention Rights",
    ],
    "Qanun-e-Shahadat (Evidence)": [
        "Admissibility of Evidence",
        "Burden of Proof",
        "Witnesses & Examination",
        "Documentary Evidence",
        "Confession & Dying Declaration",
    ],
    "Family Laws": [
        "Muslim Marriage & Divorce",
        "Khula & Judicial Divorce",
        "Child Custody & Guardianship",
        "Maintenance & Dower",
        "Inheritance & Succession",
    ],
    "Contract Act 1872": [
        "Elements of Valid Contract",
        "Void & Voidable Contracts",
        "Breach & Remedies",
        "Quasi Contracts",
        "Agency & Bailment",
    ],
    "PECA 2016 (Cybercrime)": [
        "Online Harassment (Section 20)",
        "Cyberterrorism (Section 10)",
        "Data Crimes (Section 14-16)",
        "Electronic Fraud (Section 18)",
        "Investigation Powers",
    ],
    "Anti-Terrorism Act": [
        "Definition of Terrorism",
        "ATC Jurisdiction",
        "Scheduled Offences",
        "Investigation & Prosecution",
        "Preventive Detention",
    ],
}


def get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0.3, max_tokens=2000)


def generate_mcqs(topic: str, subtopic: str, num_questions: int = 5) -> List[Dict]:
    """Generate MCQ questions for a legal topic."""
    llm = get_llm()
    prompt = f"""Generate {num_questions} multiple choice questions about "{subtopic}" under Pakistani law ({topic}).

Return ONLY a JSON array in this exact format:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "Option A text",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "correct": "A",
    "explanation": "Why A is correct, with specific law reference (e.g. Section X of Y Act)"
  }}
]

Requirements:
- Questions must be based on actual Pakistani law
- Include specific section numbers in explanations
- Mix easy, medium, and hard questions
- Options must be plausible (no obviously wrong answers)
- Return ONLY valid JSON array, no other text"""

    response = llm.invoke([{"role": "user", "content": prompt}])
    raw = response.content.strip()

    try:
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception:
        # Return fallback question if parsing fails
        return [{
            "question": f"Which act governs {subtopic} in Pakistan?",
            "options": {"A": topic, "B": "Contract Act", "C": "Civil Law", "D": "Common Law"},
            "correct": "A",
            "explanation": f"{subtopic} is governed under {topic} in Pakistan."
        }]


def explain_concept(concept: str, level: str = "student") -> str:
    """Explain a legal concept at the appropriate level."""
    llm = get_llm()

    level_instructions = {
        "beginner": "Use very simple language. No legal jargon. Use everyday examples.",
        "student": "Use academic language with examples. Include relevant sections and case references.",
        "professional": "Use technical legal language. Include all nuances, exceptions, and precedents.",
    }

    prompt = f"""Explain the Pakistani legal concept: "{concept}"

Level: {level_instructions.get(level, level_instructions['student'])}

Structure your explanation as:
## 📖 Definition
[Clear definition]

## 🏛️ Legal Basis
[Relevant Pakistani law, act, section, or article]

## 💡 Key Elements
[Essential components or requirements]

## 📝 Example
[Practical Pakistani example to illustrate]

## ⚖️ Related Concepts
[Connected legal concepts]

## 🔍 Common Exam Points
[What students are typically tested on]"""

    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


def get_case_scenario(topic: str) -> Dict:
    """Generate a legal case scenario for practice."""
    llm = get_llm()
    prompt = f"""Create a realistic Pakistani legal case scenario for the topic: {topic}

Return ONLY JSON in this format:
{{
    "scenario": "Detailed case scenario description (3-4 sentences)",
    "question": "What legal action/advice would you give?",
    "key_issues": ["issue1", "issue2", "issue3"],
    "applicable_laws": ["Section X of Y Act", "Article Z of Constitution"],
    "model_answer": "Comprehensive model answer with legal reasoning",
    "difficulty": "Easy/Medium/Hard"
}}

Make it realistic to Pakistani legal context. Return ONLY valid JSON."""

    response = llm.invoke([{"role": "user", "content": prompt}])
    raw = response.content.strip()
    try:
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception:
        return {
            "scenario": f"A case involving {topic} in Pakistan.",
            "question": "What legal action would you recommend?",
            "key_issues": ["Jurisdiction", "Applicable law", "Remedies"],
            "applicable_laws": [topic],
            "model_answer": "Consult the relevant sections of Pakistani law.",
            "difficulty": "Medium"
        }
