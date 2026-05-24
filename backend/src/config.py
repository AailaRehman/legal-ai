import os
from pathlib import Path

BASE_DIR          = Path(__file__).parent.parent
VECTOR_STORE_PATH = str(BASE_DIR / "vector_store")
RAW_DOCS_PATH     = str(BASE_DIR / "legal_docs")
DB_PATH           = str(BASE_DIR / "mizan.db")

GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL        = "llama-3.3-70b-versatile"
EMBEDDING_MODEL   = "all-MiniLM-L6-v2"

JWT_SECRET        = os.getenv("JWT_SECRET", "mizan-secret-key-change-in-production")
JWT_ALGORITHM     = "HS256"
JWT_EXPIRE_HOURS  = 24 * 7   # 1 week
