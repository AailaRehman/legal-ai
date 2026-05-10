"""
RAG Pipeline — Pakistani Legal AI
Retrieves relevant law sections + generates cited answers via Groq LLM.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv

# Load .env from project root regardless of working directory
_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


# ── LLM ───────────────────────────────────────────────────────────────────────

def get_llm(temperature: float = 0.1) -> ChatGroq:
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=LLM_MODEL,
        temperature=temperature,
        max_tokens=2048,
    )


# ── Prompts ───────────────────────────────────────────────────────────────────

LEGAL_SYSTEM_PROMPT = """You are an expert Pakistani legal AI assistant with deep knowledge of:
- Constitution of Pakistan
- Pakistan Penal Code (PPC)
- Code of Criminal Procedure (CrPC)
- Qanun-e-Shahadat (Evidence Act)
- PECA (Cybercrime Act)
- Family Laws, Labour Laws, Tax Laws
- Supreme Court and High Court judgments

RULES YOU MUST FOLLOW:
1. ALWAYS cite the exact law, section, or article you're referencing.
   Format: [Source: Law Name, Section/Article Number]
2. If you don't know or the context doesn't contain the answer, say:
   "I don't have enough information in my knowledge base. Please consult a qualified lawyer."
3. Answer in the same language the user asks (Urdu or English).
4. For serious legal matters, always add: "⚠️ Please consult a qualified lawyer for professional advice."
5. Be precise, accurate, and structured in your answers.

MODE: {mode}
- Citizen Mode: Use simple, easy-to-understand language. Avoid legal jargon.
- Lawyer Mode: Use technical legal terminology. Include precedents and sections.
- Student Mode: Explain concepts academically with examples.

CONTEXT FROM LEGAL KNOWLEDGE BASE:
{context}

Answer the question based on the above context. If the context is insufficient, say so clearly.
"""

CONDENSE_QUESTION_PROMPT = """Given the following conversation history and a follow-up question,
rephrase the follow-up question to be a standalone question in the context of Pakistani law.

Chat History:
{chat_history}

Follow Up Question: {question}
Standalone Question:"""


# ── RAG Chain ─────────────────────────────────────────────────────────────────

class PakistaniLegalRAG:
    def __init__(self, vectorstore: FAISS, mode: str = "Citizen"):
        self.vectorstore = vectorstore
        self.mode = mode
        self.llm = get_llm()
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )

    def _format_docs_with_citations(self, docs: List[Document]) -> str:
        """Format retrieved docs with source citations."""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            law_type = doc.metadata.get("law_type", "Pakistani Law")
            formatted.append(
                f"[Source {i}: {law_type} | File: {source}]\n{doc.page_content}"
            )
        return "\n\n---\n\n".join(formatted)

    def ask(self, question: str) -> Dict[str, Any]:
        """
        Ask a legal question. Returns answer + source documents.
        """
        # Retrieve relevant docs
        docs = self.retriever.get_relevant_documents(question)
        context = self._format_docs_with_citations(docs)

        # Build prompt
        system_msg = LEGAL_SYSTEM_PROMPT.format(mode=self.mode, context=context)

        # Get chat history from memory
        history = self.memory.chat_memory.messages

        # Format messages for Groq
        messages = [{"role": "system", "content": system_msg}]
        for msg in history[-6:]:  # last 3 turns
            role = "user" if msg.type == "human" else "assistant"
            messages.append({"role": role, "content": msg.content})
        messages.append({"role": "user", "content": question})

        # Call LLM
        response = self.llm.invoke(messages)
        answer = response.content

        # Save to memory
        self.memory.chat_memory.add_user_message(question)
        self.memory.chat_memory.add_ai_message(answer)

        return {
            "answer": answer,
            "source_documents": docs,
            "sources": self._extract_sources(docs),
        }

    def _extract_sources(self, docs: List[Document]) -> List[str]:
        """Return unique source list for display."""
        seen = set()
        sources = []
        for doc in docs:
            src = f"{doc.metadata.get('law_type', 'Pakistani Law')} ({doc.metadata.get('source', '')})"
            if src not in seen:
                seen.add(src)
                sources.append(src)
        return sources

    def set_mode(self, mode: str):
        self.mode = mode

    def clear_memory(self):
        self.memory.clear()


def create_rag_chain(vectorstore: FAISS, mode: str = "Citizen") -> PakistaniLegalRAG:
    return PakistaniLegalRAG(vectorstore, mode)
