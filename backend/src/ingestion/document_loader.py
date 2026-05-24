import os
from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Law name mappings from filename → display name
LAW_NAMES = {
    "constitution":         "Constitution of Pakistan 1973",
    "ppc":                  "Pakistan Penal Code 1860",
    "crpc":                 "Code of Criminal Procedure 1898",
    "peca":                 "Prevention of Electronic Crimes Act 2016",
    "family":               "Muslim Family Laws Ordinance 1961",
    "contract":             "Contract Act 1872",
    "transfer":             "Transfer of Property Act 1882",
    "evidence":             "Qanun-e-Shahadat Order 1984",
    "income_tax":           "Income Tax Ordinance 2001",
    "rent":                 "Rent Restriction Ordinance 1959",
    "labour":               "Industrial Relations Act 2012",
    "consumer":             "Consumer Protection Act 2019",
    "anti_terrorism":       "Anti-Terrorism Act 1997",
    "narcotics":            "Control of Narcotic Substances Act 1997",
    "defamation":           "Defamation Ordinance 2002",
    "succession":           "Succession Act 1925",
    "companies":            "Companies Act 2017",
    "arbitration":          "Arbitration Act 1940",
    "civil_procedure":      "Code of Civil Procedure 1908",
    "limitation":           "Limitation Act 1908",
}

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def _law_name_from_path(path: str) -> str:
    stem = Path(path).stem.lower()
    for key, name in LAW_NAMES.items():
        if key in stem:
            return name
    return Path(path).stem.replace("_", " ").title()


def ingest_documents(folder: str) -> List[Document]:
    """Load and chunk all PDFs in a folder."""
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"⚠️  Folder not found: {folder}")
        return []

    pdf_files = list(folder_path.glob("**/*.pdf"))
    if not pdf_files:
        print(f"⚠️  No PDF files found in {folder}")
        return []

    all_docs: List[Document] = []

    for pdf_path in pdf_files:
        try:
            print(f"  📄 Loading: {pdf_path.name}")
            loader = PyPDFLoader(str(pdf_path))
            pages  = loader.load()

            law_name = _law_name_from_path(str(pdf_path))

            # Add metadata to every page
            for page in pages:
                page.metadata["source"]   = law_name
                page.metadata["filename"] = pdf_path.name
                page.metadata["section"]  = f"p.{page.metadata.get('page', 0) + 1}"

            chunks = SPLITTER.split_documents(pages)
            all_docs.extend(chunks)
            print(f"     ✅ {len(chunks)} chunks from {law_name}")

        except Exception as e:
            print(f"     ❌ Error loading {pdf_path.name}: {e}")

    print(f"\n📚 Total chunks: {len(all_docs)} from {len(pdf_files)} PDFs")
    return all_docs


def ingest_single_file(path: str) -> List[Document]:
    """Load and chunk a single PDF file."""
    try:
        loader   = PyPDFLoader(path)
        pages    = loader.load()
        law_name = _law_name_from_path(path)
        for page in pages:
            page.metadata["source"]   = law_name
            page.metadata["filename"] = Path(path).name
            page.metadata["section"]  = f"p.{page.metadata.get('page', 0) + 1}"
        return SPLITTER.split_documents(pages)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return []
