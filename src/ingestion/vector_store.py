"""
Vector Store Manager — FAISS + HuggingFace Embeddings
Builds, saves, and loads the legal knowledge base.
"""

import os
from pathlib import Path
from typing import List, Optional

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", str(_project_root / "data" / "vector_store"))


def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store(documents: List[Document], save_path: str = VECTOR_STORE_PATH) -> FAISS:
    """Embed documents and save FAISS index to disk."""
    print(f"Building vector store with {len(documents)} chunks...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    Path(save_path).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(save_path)
    print(f"Vector store saved → {save_path}")
    return vectorstore


def load_vector_store(load_path: str = VECTOR_STORE_PATH) -> Optional[FAISS]:
    """Load existing FAISS index from disk."""
    if not Path(load_path).exists():
        return None
    embeddings = get_embeddings()
    return FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)


def add_documents_to_store(
    new_docs: List[Document],
    load_path: str = VECTOR_STORE_PATH,
) -> FAISS:
    """Add new documents to existing vector store (or create new)."""
    embeddings = get_embeddings()
    existing = load_vector_store(load_path)

    if existing:
        existing.add_documents(new_docs)
        existing.save_local(load_path)
        return existing
    else:
        return build_vector_store(new_docs, load_path)


def vector_store_exists(path: str = VECTOR_STORE_PATH) -> bool:
    return Path(path).exists() and any(Path(path).iterdir())
