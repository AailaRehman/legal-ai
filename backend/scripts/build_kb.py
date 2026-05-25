#!/usr/bin/env python3
"""
Mizan Knowledge Base Builder
=============================
Run this once to ingest all PDFs from legal_docs/ into the FAISS vector store.

Usage:
    cd backend
    python scripts/build_kb.py

    # Ingest a single file:
    python scripts/build_kb.py --file path/to/law.pdf

    # Force rebuild even if KB exists:
    python scripts/build_kb.py --force
"""

import sys
import os
import argparse
import time

# Add backend/ to path so src.* imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import VECTOR_STORE_PATH, RAW_DOCS_PATH
from src.ingestion.document_loader import ingest_documents, ingest_single_file
from src.ingestion.vector_store import (
    build_vector_store, add_documents_to_store, vector_store_exists
)


def main():
    parser = argparse.ArgumentParser(description="Build Mizan FAISS Knowledge Base")
    parser.add_argument("--file",  type=str, help="Ingest a single PDF file")
    parser.add_argument("--force", action="store_true", help="Force rebuild even if KB exists")
    parser.add_argument("--docs",  type=str, default=RAW_DOCS_PATH, help="Path to legal docs folder")
    args = parser.parse_args()

    print("=" * 55)
    print("  ⚖️  Mizan Knowledge Base Builder")
    print("=" * 55)

    # Single file mode
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        print(f"\n📄 Ingesting single file: {args.file}")
        docs = ingest_single_file(args.file)
        if not docs:
            print("❌ No content extracted.")
            sys.exit(1)
        print(f"➕ Adding {len(docs)} chunks to knowledge base…")
        add_documents_to_store(docs, VECTOR_STORE_PATH)
        print("✅ Done!")
        return

    # Full rebuild
    if vector_store_exists(VECTOR_STORE_PATH) and not args.force:
        print(f"\n✅ Knowledge base already exists at: {VECTOR_STORE_PATH}")
        print("   Use --force to rebuild from scratch.")
        return

    docs_path = args.docs
    if not os.path.exists(docs_path):
        print(f"\n❌ Legal docs folder not found: {docs_path}")
        print(f"   Create the folder and add your Pakistani law PDFs:")
        print(f"   mkdir -p {docs_path}")
        print(f"   # Copy your 25 PDFs into {docs_path}/")
        sys.exit(1)

    print(f"\n📂 Scanning: {docs_path}")
    start = time.time()

    docs = ingest_documents(docs_path)

    if not docs:
        print("\n❌ No documents loaded. Check that PDFs are in the legal_docs/ folder.")
        sys.exit(1)

    print(f"\n🔨 Building FAISS vector store ({len(docs)} chunks)…")
    print("   This may take 2–5 minutes on first run (downloading embeddings model)…")

    build_vector_store(docs, VECTOR_STORE_PATH)

    elapsed = time.time() - start
    print(f"\n{'='*55}")
    print(f"  ✅ Knowledge Base built successfully!")
    print(f"  📊 {len(docs)} chunks indexed")
    print(f"  📁 Saved to: {VECTOR_STORE_PATH}")
    print(f"  ⏱  Time: {elapsed:.1f}s")
    print(f"{'='*55}")
    print("\n  Start the API server:")
    print("  uvicorn main:app --reload")


if __name__ == "__main__":
    main()
