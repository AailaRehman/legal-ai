import os
from pathlib import Path

BASE_DIR          = Path(__file__).parent.parent
REPO_ROOT         = BASE_DIR.parent  # one level up from backend/

# Check backend/legal_docs/ first, then repo root legal_docs/
_backend_docs = BASE_DIR / "legal_docs"
_root_docs    = REPO_ROOT / "legal_docs"
RAW_DOCS_PATH = str(_backend_docs if _backend_docs.exists() and any(_backend_docs.glob("*.pdf")) else _root_docs)

VECTOR_STORE_PATH = str(BASE_DIR / "vector_store")
DB_PATH           = str(BASE_DIR / "mizan.db")

GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL        = "llama-3.3-70b-versatile"
EMBEDDING_MODEL   = "all-MiniLM-L6-v2"

JWT_SECRET        = os.getenv("JWT_SECRET", "mizan-secret-key-change-in-production")
JWT_ALGORITHM     = "HS256"
JWT_EXPIRE_HOURS  = 24 * 7
