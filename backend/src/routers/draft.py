# ── draft.py ──────────────────────────────────────────────────
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.auth.auth_router import get_current_user
from src.database.db_manager import save_document

router = APIRouter()

TEMPLATES = {
    "Legal Notice":       "Draft a formal legal notice under Pakistani law. Include: To/From details, subject, facts, legal basis, demand, and consequences of non-compliance.",
    "Affidavit":          "Draft a sworn affidavit for Pakistani courts. Include: sworn statement format, deponent details, facts, verification clause, and notarization requirement.",
    "Rent Agreement":     "Draft a comprehensive rent agreement under Pakistani Rent Restriction laws. Include: parties, property description, rent, duration, terms, and termination clauses.",
    "FIR Draft":          "Draft a detailed FIR complaint under Section 154 CrPC Pakistan. Include: complainant details, accused, incident details, sections violated, and relief sought.",
    "NDA Agreement":      "Draft a Non-Disclosure Agreement valid under Pakistani Contract Act 1872. Include: parties, confidential information definition, obligations, duration, and remedies.",
    "Power of Attorney":  "Draft a Power of Attorney document under Pakistani law. Include: principal, attorney, specific powers granted, duration, and revocation terms.",
    "Petition":           "Draft a formal petition for Pakistani courts. Include: parties, jurisdiction, facts, legal grounds, prayer/relief sought, and verification.",
    "Contract Agreement": "Draft a comprehensive contract agreement under Pakistani Contract Act 1872. Include: parties, offer/acceptance, consideration, terms, breach remedies, and governing law.",
}

class DraftRequest(BaseModel):
    doc_type: str
    fields:   dict = {}

@router.post("/draft")
def draft_document(req: DraftRequest, user=Depends(get_current_user)):
    llm     = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.2, max_tokens=3000)
    base    = TEMPLATES.get(req.doc_type, f"Draft a {req.doc_type} under Pakistani law.")
    fields  = "\n".join([f"- {k}: {v}" for k, v in req.fields.items()]) if req.fields else "Use placeholder brackets [PARTY NAME], [DATE], etc."
    prompt  = f"""{base}

Provided details:
{fields}

Generate a complete, professional legal document ready to use.
Use proper legal formatting. Leave blanks as [FILL IN] where information is missing."""
    result  = llm.invoke(prompt)
    content = result.content
    save_document(user["id"], f"{req.doc_type} — {list(req.fields.values())[0] if req.fields else 'Draft'}", req.doc_type, content)
    return {"content": content}
