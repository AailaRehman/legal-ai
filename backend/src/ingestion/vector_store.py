import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store(docs, path: str) -> FAISS:
    embeddings = get_embeddings()
    vs = FAISS.from_documents(docs, embeddings)
    vs.save_local(path)
    return vs


def load_vector_store(path: str) -> FAISS:
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)


def vector_store_exists(path: str) -> bool:
    return os.path.exists(os.path.join(path, "index.faiss"))
