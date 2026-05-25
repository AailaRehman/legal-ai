# multilingual.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.auth.auth_router import get_current_user

router = APIRouter()

MULTILINGUAL_PROMPT = """You are Mizan, a Pakistani legal AI assistant.
The user has asked a question in {language}. 
Reply in the SAME language they used — if they wrote in Urdu script, reply in Urdu script.
If they wrote in Roman Urdu, reply in Roman Urdu. If English, reply in English.

Ground your answer in Pakistani law and cite specific laws/sections.
Be helpful, clear, and practical.

Question: {query}

Answer:"""

class MultilingualRequest(BaseModel):
    query:    str
    language: str = "auto"
    history:  list = []

@router.post("/multilingual")
def multilingual_chat(req: MultilingualRequest, user=Depends(get_current_user)):
    lang_map = {"urdu": "Urdu (اردو)", "roman_urdu": "Roman Urdu", "english": "English", "auto": "the same language as the question"}
    lang_label = lang_map.get(req.language, req.language)
    llm    = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.3, max_tokens=1500)
    prompt = MULTILINGUAL_PROMPT.format(language=lang_label, query=req.query)
    result = llm.invoke(prompt)
    return {"answer": result.content, "response_language": req.language}
