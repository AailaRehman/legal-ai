from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import json
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.auth.auth_router import get_current_user

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text:     str
    filename: Optional[str] = "document"

@router.post("/analyze")
def analyze_document(req: AnalyzeRequest, user=Depends(get_current_user)):
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.2, max_tokens=3000)

    prompt = f"""Analyze this legal document from a Pakistani law perspective.

Return ONLY valid JSON (no markdown):
{{
  "summary": "2-3 sentence plain-language summary",
  "risk_score": 45,
  "risk_level": "medium",
  "risk_factors": ["risk1", "risk2", "risk3"],
  "missing_clauses": ["missing1", "missing2"],
  "positive_points": ["good1", "good2"],
  "entities": {{
    "persons": ["name1"],
    "organizations": ["org1"],
    "dates": ["date1"],
    "amounts": ["amount1"],
    "law_sections": ["PPC Section X"]
  }}
}}

risk_score is 0-100. risk_level is "low" (<30), "medium" (30-70), or "high" (>70).

Document:
{req.text[:4000]}"""

    result = llm.invoke(prompt)
    try:
        text = result.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return {
            "summary": "Document analyzed. Please review manually.",
            "risk_score": 50, "risk_level": "medium",
            "risk_factors": ["Could not parse detailed analysis"],
            "missing_clauses": [], "positive_points": [],
            "entities": {"persons": [], "organizations": [], "dates": [], "amounts": [], "law_sections": []},
        }
