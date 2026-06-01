from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.auth.auth_router import get_current_user
from src.ingestion.vector_store import load_vector_store, vector_store_exists
from src.config import VECTOR_STORE_PATH

router = APIRouter()

LAW_LIST = [
    "Constitution of Pakistan 1973",
    "Pakistan Penal Code 1860",
    "Code Of Criminal Procedure",
    "Prevention-Of-Electronic-Crime-Act-2016",
    "Muslim Family Laws Ordinance 1961",
    "Contract Act 1872",
    "Transfer of Property Act 1882",
    "Qanun-E-Shahadat Order 1984",
    "Income Tax Ordinance 2001",
    "Rent Restriction Ordinance 1959",
    "Industrial Relations Act, 2012",
    "Consumer Protection Act 2019",
    "Anti-Terrorism Act 1997",
    "Control of Narcotic Substances Act 1997",
    "Companies Act 2017",
    "Civil Servants Act, 1973",
    "Anti-Money Laundering (Aml) Act, 2010",
    "Child Marriage Restraint Act",
    "Dissolution Of Muslim Marriages Act 1939",
    "Estacode",
    "Land Aquisition Act",
    "Mental Health Ordinance 2001",
    "Rules Of Business 1973",
    "West Pakistan Family Courts Act 1964",
]

class SearchRequest(BaseModel):
    query: str
    law_filter: Optional[str] = None
    k: int = 8

class BrowseRequest(BaseModel):
    law_name: str
    page: int = 1
    page_size: int = 10

@router.get("/research/laws")
def get_laws(user=Depends(get_current_user)):
    return {"laws": LAW_LIST}

@router.post("/research/search")
def search_laws(req: SearchRequest, user=Depends(get_current_user)):
    if not vector_store_exists(VECTOR_STORE_PATH):
        raise HTTPException(status_code=503, detail="Knowledge base not built yet")

    vs = load_vector_store(VECTOR_STORE_PATH)

    if req.law_filter:
        # Filter by specific law using metadata
        results = vs.similarity_search_with_score(req.query, k=req.k * 3)
        results = [(doc, score) for doc, score in results
                   if req.law_filter.lower() in doc.metadata.get("source", "").lower()]
        results = results[:req.k]
    else:
        results = vs.similarity_search_with_score(req.query, k=req.k)

    return {
        "query": req.query,
        "results": [
            {
                "text":     doc.page_content,
                "source":   doc.metadata.get("source", "Unknown"),
                "section":  doc.metadata.get("section", ""),
                "filename": doc.metadata.get("filename", ""),
                "score":    round(float(score), 4),
            }
            for doc, score in results
        ]
    }

@router.post("/research/browse")
def browse_law(req: BrowseRequest, user=Depends(get_current_user)):
    if not vector_store_exists(VECTOR_STORE_PATH):
        raise HTTPException(status_code=503, detail="Knowledge base not built yet")

    vs      = load_vector_store(VECTOR_STORE_PATH)
    # Get chunks for this law by doing a broad similarity search filtered by source
    results = vs.similarity_search_with_score(req.law_name, k=200)
    chunks  = [
        {
            "text":    doc.page_content,
            "source":  doc.metadata.get("source", ""),
            "section": doc.metadata.get("section", ""),
            "score":   round(float(score), 4),
        }
        for doc, score in results
        if req.law_name.lower()[:15] in doc.metadata.get("source", "").lower()
    ]

    # Paginate
    start = (req.page - 1) * req.page_size
    end   = start + req.page_size
    return {
        "law":        req.law_name,
        "total":      len(chunks),
        "page":       req.page,
        "page_size":  req.page_size,
        "chunks":     chunks[start:end],
    }
