"""
Run this ONCE on your local machine to build the FAISS vector store.
After running, the data/vector_store/ folder will be created.

Usage:
    python build_index.py

Make sure all PDFs are in data/raw/pdfs/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.document_loader import ingest_documents
from src.ingestion.vector_store import build_vector_store

RAW_DOCS_FOLDER = "data/raw/pdfs"
VECTOR_STORE_PATH = "data/vector_store"


def main():
    print("=" * 60)
    print("  Pakistani Legal AI — Index Builder")
    print("=" * 60)

    docs_path = Path(RAW_DOCS_FOLDER)
    if not docs_path.exists() or not any(docs_path.iterdir()):
        print(f"\n❌ No documents found in {RAW_DOCS_FOLDER}")
        print("Please add your PDF/TXT law documents there first.")
        return

    print(f"\n📂 Loading documents from: {RAW_DOCS_FOLDER}\n")
    documents = ingest_documents(RAW_DOCS_FOLDER)

    if not documents:
        print("❌ No text could be extracted. Check your PDF files.")
        return

    print(f"\n🔢 Total chunks to embed: {len(documents)}")
    print("\n⏳ Building FAISS vector store (may take 2-5 minutes)...\n")

    vectorstore = build_vector_store(documents, VECTOR_STORE_PATH)

    print(f"\n✅ Vector store saved to: {VECTOR_STORE_PATH}/")
    print("✅ You can now run: streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
