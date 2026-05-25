# ── strategy.py ───────────────────────────────────────────────
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.auth.auth_router import get_current_user
from src.database.db_manager import save_strategy

router = APIRouter()

STRATEGY_PROMPT = """You are an expert Pakistani legal strategist.
Analyze the situation and provide a comprehensive legal strategy in exactly these 10 sections:

## 1. Legal Assessment
## 2. Applicable Laws & Sections  
## 3. Immediate Actions (Next 24-48 hours)
## 4. Court/Authority to Approach
## 5. Required Documents
## 6. Step-by-Step Legal Process
## 7. Realistic Timeline
## 8. Estimated Costs
## 9. Risks & Challenges
## 10. Alternative Resolutions

Situation: {situation}
Your role: {role}
Urgency: {urgency}
Resources: {resources}

Be specific to Pakistani law. Name exact sections, courts, and procedures."""

PROCEDURE_PROMPTS = {
    "File an FIR": "Give a complete step-by-step guide to file an FIR in Pakistan including Section 154 CrPC, rights if police refuse, required information, and what to do next.",
    "Apply for Bail": "Explain the complete bail application process in Pakistan — types of bail (pre-arrest, post-arrest), applicable sections, bail application format, and hearing procedure.",
    "File a Civil Suit": "Explain how to file a civil suit in Pakistan — jurisdiction, court fee, plaint format, evidence, timeline, and the full trial procedure under CPC.",
    "File a Constitutional Petition": "Explain how to file a constitutional petition under Article 199 (High Court) or Article 184(3) (Supreme Court) in Pakistan.",
    "Challenge a Court Order": "Explain how to appeal or challenge a court order in Pakistan — revision, appeal, and writ jurisdiction with applicable timeframes.",
    "File a Consumer Complaint": "Explain how to file a complaint with the Consumer Protection Court or CCPC in Pakistan including evidence and jurisdiction.",
    "Apply for Khula (Divorce)": "Explain the complete Khula process for women in Pakistan under the Muslim Family Laws Ordinance 1961 — step by step.",
    "Register a Property": "Explain property registration in Pakistan — stamp duty, registration fee, documents needed, and the full process at the Sub-Registrar office.",
}

class StrategyRequest(BaseModel):
    situation: str
    role:      str = "Complainant"
    urgency:   str = "Medium"
    resources: str = "Limited"

class ProcedureRequest(BaseModel):
    procedure: str

@router.post("/strategy")
def get_strategy(req: StrategyRequest, user=Depends(get_current_user)):
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.3, max_tokens=3000)
    prompt = STRATEGY_PROMPT.format(situation=req.situation, role=req.role, urgency=req.urgency, resources=req.resources)
    result = llm.invoke(prompt)
    strategy = result.content
    save_strategy(user["id"], req.situation[:80], req.situation, strategy)
    return {"strategy": strategy}

@router.post("/procedure")
def get_procedure(req: ProcedureRequest, user=Depends(get_current_user)):
    llm    = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.2, max_tokens=2000)
    prompt = PROCEDURE_PROMPTS.get(req.procedure, f"Explain the procedure for: {req.procedure} under Pakistani law.")
    result = llm.invoke(prompt)
    return {"procedure": result.content}
