import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Add current directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from services.embedding_service import get_embeddings_client
from api.health import router as health_router
from api.process import router as process_router
from api.chat import router as chat_router
from api.session import router as session_router

logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("==================================================")
    logger.info(f"Starting {settings.PROJECT_NAME} Backend Engine...")
    logger.info(f"Allowed CORS Origins: {settings.ALLOWED_ORIGINS}")
    logger.info(f"Temp Directory: {settings.TEMP_DIR}")
    logger.info("==================================================")

    # Pre-warm Embedding client
    logger.info("Pre-warming Embedding client on startup...")
    try:
        model_type, _ = get_embeddings_client()
        logger.info(f"Embedding client ({model_type}) pre-warmed successfully.")
    except Exception as e:
        logger.error(f"Failed to pre-warm Embedding client: {str(e)}")

    logger.info("Startup sequence complete. Server ready.")
    yield

    logger.info("Shutting down MediGuru Backend Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Medical Document Intelligence MVP (Gemini 2.5 Flash Vision, RAG)",
    version="1.0.0-mvp",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router)
app.include_router(process_router)
app.include_router(chat_router)
app.include_router(session_router)

@app.get("/", summary="Root Endpoint")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} FastAPI Backend!"}
