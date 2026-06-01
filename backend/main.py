from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.database.db_manager import init_db
from src.auth.auth_router        import router as auth_router
from src.routers.chat            import router as chat_router
from src.routers.analyze         import router as analyze_router
from src.routers.draft           import router as draft_router
from src.routers.strategy        import router as strategy_router
from src.routers.education       import router as education_router
from src.routers.multilingual    import router as multilingual_router
from src.routers.user            import router as user_router
from src.routers.admin           import router as admin_router
from src.routers.kb              import router as kb_router
from src.routers.research        import router as research_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("✅ Mizan FastAPI started — DB initialised")
    yield

app = FastAPI(
    title="Mizan Legal AI",
    description="Pakistan Legal AI — RAG + LangChain + Groq LLaMA 3.3-70B",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,         prefix="/auth",      tags=["auth"])
app.include_router(chat_router,                              tags=["chat"])
app.include_router(analyze_router,                           tags=["analyze"])
app.include_router(draft_router,                             tags=["draft"])
app.include_router(strategy_router,                          tags=["strategy"])
app.include_router(education_router,    prefix="/education", tags=["education"])
app.include_router(multilingual_router,                      tags=["multilingual"])
app.include_router(user_router,         prefix="/user",      tags=["user"])
app.include_router(admin_router,        prefix="/admin",     tags=["admin"])
app.include_router(kb_router,                                tags=["kb"])
app.include_router(research_router,                          tags=["research"])

@app.get("/health")
async def health():
    from src.ingestion.vector_store import vector_store_exists
    from src.config import VECTOR_STORE_PATH
    return {"status": "ok", "kb_ready": vector_store_exists(VECTOR_STORE_PATH)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
