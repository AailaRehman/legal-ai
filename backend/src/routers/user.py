# ── user.py ───────────────────────────────────────────────────
from fastapi import APIRouter, Depends
from src.auth.auth_router import get_current_user
from src.database.db_manager import (
    get_chat_sessions, get_documents, get_strategies,
    delete_session, delete_document
)

router = APIRouter()

@router.get("/chats")
def user_chats(user=Depends(get_current_user)):
    sessions = get_chat_sessions(user["id"])
    return [{"session_id": s["session_id"], "title": s["title"] or "Untitled chat",
             "mode": s["mode"], "created_at": s["last_at"], "message_count": s["message_count"]}
            for s in sessions]

@router.delete("/chats/{session_id}")
def delete_chat(session_id: str, user=Depends(get_current_user)):
    delete_session(user["id"], session_id)
    return {"deleted": True}

@router.get("/documents")
def user_documents(user=Depends(get_current_user)):
    return get_documents(user["id"])

@router.delete("/documents/{doc_id}")
def del_document(doc_id: int, user=Depends(get_current_user)):
    delete_document(user["id"], doc_id)
    return {"deleted": True}

@router.get("/strategies")
def user_strategies(user=Depends(get_current_user)):
    return get_strategies(user["id"])
