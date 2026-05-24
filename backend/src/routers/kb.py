from fastapi import APIRouter, Depends, BackgroundTasks
from src.auth.auth_router import require_admin
from src.ingestion.document_loader import ingest_documents
from src.ingestion.vector_store import build_vector_store, vector_store_exists
from src.config import VECTOR_STORE_PATH, RAW_DOCS_PATH
import os

router = APIRouter()

_build_status = {"running": False, "done": False, "error": "", "chunks": 0}


def _build_task():
    global _build_status
    _build_status = {"running": True, "done": False, "error": "", "chunks": 0}
    try:
        docs = ingest_documents(RAW_DOCS_PATH)
        if not docs:
            _build_status["error"] = "No PDFs found in legal_docs/"
            _build_status["running"] = False
            return
        build_vector_store(docs, VECTOR_STORE_PATH)
        _build_status["chunks"]  = len(docs)
        _build_status["done"]    = True
        _build_status["running"] = False
    except Exception as e:
        _build_status["error"]   = str(e)
        _build_status["running"] = False


@router.post("/kb/build")
def build_kb(background_tasks: BackgroundTasks, admin=Depends(require_admin)):
    if _build_status["running"]:
        return {"message": "Build already in progress"}
    background_tasks.add_task(_build_task)
    return {"message": "Knowledge base build started"}


@router.get("/kb/status")
def kb_status(admin=Depends(require_admin)):
    return {
        **_build_status,
        "exists": vector_store_exists(VECTOR_STORE_PATH),
    }
