from fastapi import APIRouter, Depends
from pydantic import BaseModel
import json
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.auth.auth_router import get_current_user

router = APIRouter()

class MCQRequest(BaseModel):
    topic:         str
    subtopic:      str
    num_questions: int = 5

class ConceptRequest(BaseModel):
    concept: str
    level:   str = "student"

class ScenarioRequest(BaseModel):
    topic: str

@router.post("/mcqs")
def generate_mcqs(req: MCQRequest, user=Depends(get_current_user)):
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.4, max_tokens=3000)
    prompt = f"""Generate {req.num_questions} multiple choice questions about {req.topic} — {req.subtopic} under Pakistani law.

Return ONLY valid JSON array, no markdown, no explanation:
[
  {{
    "question": "Question text here",
    "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
    "correct": "A",
    "explanation": "Brief explanation with Pakistani law reference"
  }}
]"""
    result = llm.invoke(prompt)
    try:
        text = result.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        questions = json.loads(text.strip())
        return {"questions": questions}
    except Exception:
        return {"questions": [], "error": "Could not parse MCQs. Please try again."}

@router.post("/explain")
def explain_concept(req: ConceptRequest, user=Depends(get_current_user)):
    level_prompts = {
        "student": f"Explain '{req.concept}' for a Pakistani law student. Cover: definition, legal basis, key sections, how it works in practice, important cases, and exam-relevant points.",
        "citizen": f"Explain '{req.concept}' in simple language for an ordinary Pakistani citizen. Avoid jargon. Focus on: what it means for everyday life, when it applies, and what to do practically.",
        "lawyer":  f"Provide a detailed professional explanation of '{req.concept}' for a Pakistani lawyer. Include: legal definition, statutory basis, case law, procedural aspects, and practical considerations.",
    }
    llm    = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.3, max_tokens=1500)
    result = llm.invoke(level_prompts.get(req.level, level_prompts["student"]))
    return {"explanation": result.content}

@router.post("/scenario")
def case_scenario(req: ScenarioRequest, user=Depends(get_current_user)):
    llm    = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.5, max_tokens=2000)
    prompt = f"""Create a realistic Pakistani legal case scenario about {req.topic}.

Return ONLY valid JSON, no markdown:
{{
  "scenario": "Detailed factual scenario (150-200 words)",
  "question": "The main legal question to answer",
  "key_issues": ["issue1", "issue2", "issue3"],
  "applicable_laws": ["Law 1 with section", "Law 2 with section"],
  "model_answer": "Comprehensive model answer (200-250 words)",
  "difficulty": "Easy|Medium|Hard"
}}"""
    result = llm.invoke(prompt)
    try:
        text = result.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        raise Exception("Could not generate scenario. Please retry.")
