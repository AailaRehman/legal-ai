from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from src.auth.auth_router import get_current_user
from src.database.db_manager import save_message
from src.ingestion.vector_store import load_vector_store, vector_store_exists
from src.rag.rag_chain import create_rag_chain, extract_sources
from src.config import VECTOR_STORE_PATH

router = APIRouter()

# In-memory chain cache per session (resets on server restart)
_chains: dict = {}


class ChatRequest(BaseModel):
    query:      str
    mode:       str = "citizen"
    history:    list = []
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer:     str
    sources:    list
    session_id: str


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, user=Depends(get_current_user)):
    session_id = req.session_id or str(uuid.uuid4())

    if not vector_store_exists(VECTOR_STORE_PATH):
        return ChatResponse(
            answer="⚠️ Knowledge base not built yet. Please run the document ingestion first.",
            sources=[],
            session_id=session_id,
        )

    # Load or create chain for this session
    chain_key = f"{user['id']}-{session_id}"
    if chain_key not in _chains or _chains[chain_key]["mode"] != req.mode:
        vs = load_vector_store(VECTOR_STORE_PATH)
        _chains[chain_key] = {
            "chain": create_rag_chain(vs, req.mode),
            "mode":  req.mode,
        }

    chain = _chains[chain_key]["chain"]

    try:
        result = chain({"question": req.query})
        answer  = result.get("answer", "")
        sources = extract_sources(result.get("source_documents", []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    # Persist messages
    save_message(user["id"], session_id, "user",      req.query, req.mode)
    save_message(user["id"], session_id, "assistant", answer,    req.mode)

    return ChatResponse(answer=answer, sources=sources, session_id=session_id)
