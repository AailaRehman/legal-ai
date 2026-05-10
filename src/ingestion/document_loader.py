"""
PDF Ingestion Pipeline — Pakistani Legal AI
Handles: PDF, text files, OCR for scanned docs
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any

import fitz  # PyMuPDF
import pdfplumber
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))


# ── Metadata extractor ────────────────────────────────────────────────────────

def extract_metadata(filename: str, text: str) -> Dict[str, Any]:
    """Auto-detect law type and extract metadata from filename/content."""
    name = filename.lower()

    law_map = {
        "constitution": "Constitution of Pakistan",
        "pakistan penal code": "Pakistan Penal Code",
        "penal code": "Pakistan Penal Code",
        "qanun-e-shahadat": "Qanun-e-Shahadat (Evidence Act)",
        "qanun": "Qanun-e-Shahadat (Evidence Act)",
        "code of criminal procedure": "Code of Criminal Procedure (CrPC)",
        "crpc": "Code of Criminal Procedure (CrPC)",
        "prevention-of-electronic-crime": "Prevention of Electronic Crimes Act (PECA)",
        "peca": "Prevention of Electronic Crimes Act (PECA)",
        "anti-terrorism": "Anti-Terrorism Act",
        "anti-money laundering": "Anti-Money Laundering Act",
        "aml": "Anti-Money Laundering Act",
        "family laws": "Family Laws Ordinance",
        "family courts": "West Pakistan Family Courts Act",
        "dissolution of muslim": "Dissolution of Muslim Marriages Act",
        "child marriage": "Child Marriage Restraint Act",
        "income tax": "Income Tax Ordinance",
        "companies act": "Companies Act 2017",
        "contract act": "Contract Act 1872",
        "industrial relations": "Industrial Relations Act",
        "narcotics": "Narcotics Control Act",
        "land acqu": "Land Acquisition Act",
        "transfer of property": "Transfer of Property Act",
        "rent control": "Rent Control Act",
        "consumer protection": "Consumer Protection Act",
        "civil servants": "Civil Servants Act",
        "rules of business": "Rules of Business",
        "mental health": "Mental Health Ordinance",
        "estacode": "Estacode (Civil Service Rules)",
        "landmark": "Supreme Court Landmark Judgments",
        "judgment": "Supreme Court Judgments",
        "ppc": "Pakistan Penal Code",
        "tax": "Tax Laws",
        "labour": "Labour Laws",
    }

    # Add typo variants and sort by length (longer = more specific, match first)
    law_map["aquisition"] = "Land Acquisition Act"    # handles filename typo
    law_map["qanun-e-shahadat"] = "Qanun-e-Shahadat (Evidence Act)"
    law_map["(qanun"] = "Qanun-e-Shahadat (Evidence Act)"  # parenthetical match
    law_type = "Pakistani Law"
    for key in sorted(law_map.keys(), key=len, reverse=True):
        if key in name:
            law_type = law_map[key]
            break

    # Extract section numbers mentioned in text
    sections = re.findall(r"[Ss]ection\s+(\d+[A-Za-z]?)", text[:2000])

    return {
        "source": filename,
        "law_type": law_type,
        "sections_preview": ", ".join(sections[:5]) if sections else "N/A",
    }


# ── PDF readers ───────────────────────────────────────────────────────────────

def read_pdf_pymupdf(filepath: str) -> str:
    """Primary PDF reader using PyMuPDF."""
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def read_pdf_pdfplumber(filepath: str) -> str:
    """Fallback PDF reader using pdfplumber."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def read_text_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def load_document(filepath: str) -> str:
    """Load any supported document type."""
    ext = Path(filepath).suffix.lower()
    filename = Path(filepath).name

    if ext == ".pdf":
        text = read_pdf_pymupdf(filepath)
        if len(text) < 100:  # likely scanned — try plumber
            text = read_pdf_pdfplumber(filepath)
        return text

    elif ext in [".txt", ".md"]:
        return read_text_file(filepath)

    else:
        raise ValueError(f"Unsupported file type: {ext}")


# ── Chunker ───────────────────────────────────────────────────────────────────

def chunk_document(text: str, metadata: Dict) -> List[Document]:
    """Split text into overlapping chunks preserving legal context."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "Section ", "Article ", ". ", " "],
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk, metadata=metadata) for chunk in chunks]


# ── Main ingestion ─────────────────────────────────────────────────────────────

def ingest_documents(folder: str) -> List[Document]:
    """
    Ingest all documents from a folder.
    Returns list of LangChain Document objects ready for embedding.
    """
    folder_path = Path(folder)
    supported = {".pdf", ".txt", ".md"}
    all_docs: List[Document] = []

    files = [f for f in folder_path.iterdir() if f.suffix.lower() in supported]

    if not files:
        return []

    for file in files:
        try:
            text = load_document(str(file))
            if not text or len(text) < 50:
                continue

            metadata = extract_metadata(file.name, text)
            chunks = chunk_document(text, metadata)
            all_docs.extend(chunks)
            print(f"  ✓ {file.name} → {len(chunks)} chunks")

        except Exception as e:
            print(f"  ✗ {file.name} → Error: {e}")

    print(f"\nTotal chunks ready: {len(all_docs)}")
    return all_docs


def ingest_single_file(filepath: str) -> List[Document]:
    """Ingest a single uploaded file (used in Streamlit uploader)."""
    filename = Path(filepath).name
    text = load_document(filepath)
    if not text:
        return []
    metadata = extract_metadata(filename, text)
    return chunk_document(text, metadata)
