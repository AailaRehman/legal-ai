import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL

_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings

def build_vector_store(docs, path: str) -> FAISS:
    embeddings = get_embeddings()
    vs = FAISS.from_documents(docs, embeddings)
    os.makedirs(path, exist_ok=True)
    vs.save_local(path)
    print(f"✅ Vector store saved to {path}")
    return vs

def load_vector_store(path: str) -> FAISS:
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

def add_documents_to_store(docs, path: str) -> FAISS:
    embeddings = get_embeddings()
    if vector_store_exists(path):
        vs = load_vector_store(path)
        vs.add_documents(docs)
    else:
        vs = FAISS.from_documents(docs, embeddings)
    vs.save_local(path)
    return vs

def vector_store_exists(path: str) -> bool:
    return os.path.exists(os.path.join(path, "index.faiss"))
