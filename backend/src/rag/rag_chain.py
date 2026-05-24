from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from src.config import GROQ_API_KEY, GROQ_MODEL

SYSTEM_PROMPTS = {
    "citizen": """You are Mizan, a helpful Pakistani legal AI assistant for ordinary citizens.
Explain legal matters in simple, clear language. Avoid jargon.
Always cite the specific Pakistani law, act, or section you are referring to.
Be practical — tell people what to do step by step.
End with: "Note: This is general legal information, not legal advice. Consult a qualified Pakistani lawyer."
Context from Pakistani law documents:
{context}""",

    "lawyer": """You are Mizan, a Pakistani legal research assistant for lawyers and legal professionals.
Provide detailed, technically precise answers with full legal citations.
Reference specific sections, sub-sections, case law where applicable.
Use legal terminology. Be comprehensive and analytical.
Context from Pakistani law documents:
{context}""",

    "student": """You are Mizan, a Pakistani legal education assistant for law students.
Explain legal concepts clearly with examples. Help students understand theory and application.
Reference the relevant laws and explain why they exist and how they are applied.
Use teaching language — explain concepts, not just state them.
Context from Pakistani law documents:
{context}""",
}

CONDENSE_PROMPT = PromptTemplate.from_template("""
Given the following conversation and a follow-up question, rephrase the follow-up question
to be a standalone question in its original language.

Chat History: {chat_history}
Follow Up Input: {question}
Standalone question:""")


def create_rag_chain(vectorstore, mode: str = "citizen"):
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=0.3,
        max_tokens=2048,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    qa_prompt = PromptTemplate(
        template=SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["citizen"]) + "\n\nQuestion: {question}\nAnswer:",
        input_variables=["context", "question"],
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=5,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        condense_question_prompt=CONDENSE_PROMPT,
        return_source_documents=True,
        verbose=False,
    )
    return chain


def extract_sources(source_docs) -> list:
    sources = []
    seen    = set()
    for doc in source_docs:
        meta    = doc.metadata
        law     = meta.get("source", "Pakistani Law")
        section = meta.get("section", "")
        key     = f"{law}-{section}"
        if key not in seen:
            seen.add(key)
            sources.append({"law": law, "section": section, "snippet": doc.page_content[:120]})
    return sources[:4]
