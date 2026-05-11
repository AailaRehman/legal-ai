"""
Startup script for HuggingFace Spaces.
Runs before the app starts: seeds users, builds index if needed.
Called automatically by app.py on first load.
"""

import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
sys.path.insert(0, str(_root))


def run_startup():
    """Run all startup tasks for HF Spaces deployment."""

    # 1. Ensure data directories exist
    for folder in ["data/raw/pdfs", "data/vector_store", "data/processed"]:
        Path(folder).mkdir(parents=True, exist_ok=True)

    # 2. Init database and seed demo users
    try:
        from src.database.db_manager import init_db, create_user
        init_db()

        demo_users = [
            ("admin",    "admin@mizan.pk",    "admin123",  "admin"),
            ("lawyer1",  "lawyer@mizan.pk",   "law12345",  "lawyer"),
            ("student1", "student@mizan.pk",  "stu12345",  "student"),
            ("citizen1", "citizen@mizan.pk",  "cit12345",  "citizen"),
        ]
        for username, email, password, role in demo_users:
            create_user(username, email, password, role)
    except Exception as e:
        print(f"[startup] DB init warning: {e}")

    # 3. Check if vector store needs building
    from src.ingestion.vector_store import vector_store_exists
    if not vector_store_exists():
        pdf_dir = Path("data/raw/pdfs")
        if any(pdf_dir.glob("*.pdf")) or any(pdf_dir.glob("*.txt")):
            try:
                print("[startup] Building vector store from documents...")
                from src.ingestion.document_loader import ingest_documents
                from src.ingestion.vector_store import build_vector_store
                docs = ingest_documents(str(pdf_dir))
                if docs:
                    build_vector_store(docs)
                    print(f"[startup] Vector store built: {len(docs)} chunks")
            except Exception as e:
                print(f"[startup] Vector store build warning: {e}")
        else:
            print("[startup] No documents found in data/raw/pdfs/ — upload via sidebar")


if __name__ == "__main__":
    run_startup()
