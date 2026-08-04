import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Add current directory to path to enable direct importing of local modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

import core.logger  # Initialize structured logging configuration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.exceptions import setup_exception_handlers
from core.middleware import RequestLoggingMiddleware
from services.ocr_service import initialize_ocr
from database.database import engine, Base
from api.upload import router as upload_router
from api.chat import router as chat_router
from api.reports import router as reports_router
from api.auth import router as auth_router
from api.users import router as users_router

logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application Startup Logs
    logger.info(f"==================================================")
    logger.info(f"Starting {settings.PROJECT_NAME} FastAPI Backend Engine...")
    logger.info(f"Upload Directory: {settings.UPLOAD_DIR}")
    logger.info(f"ChromaDB Directory: {settings.CHROMA_DB_DIR}")
    logger.info(f"==================================================")

    # 1. Initialize database tables
    logger.info("Initializing PostgreSQL database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL database tables verified & initialized successfully.")
    except Exception as db_err:
        logger.critical(f"Failed to initialize database tables: {str(db_err)}", exc_info=True)

    # 2. Pre-warm PaddleOCR models
    logger.info("Pre-warming PaddleOCR models on startup...")
    try:
        initialize_ocr()
        logger.info("PaddleOCR models successfully initialized and ready for requests.")
    except Exception as e:
        logger.error(f"Failed to pre-warm PaddleOCR models on startup: {str(e)}", exc_info=True)

    logger.info(f"{settings.PROJECT_NAME} startup completed. Ready to receive HTTP traffic.")
    yield

    # Application Shutdown Logs
    logger.info(f"Shutting down {settings.PROJECT_NAME} FastAPI Backend Engine...")
    logger.info("Cleaning up application resources...")
    logger.info(f"Shutdown sequence completed cleanly.")

# Initialize FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Multi-Modal Medical Document Intelligence Platform using OCR, LLMs & RAG",
    version="1.0.0",
    lifespan=lifespan
)

# 1. Register Request Logging Middleware (logs incoming requests, outgoing responses & request IDs)
app.add_middleware(RequestLoggingMiddleware)

# 2. Register Global Exception Handlers
setup_exception_handlers(app)

# 3. Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Register API routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(reports_router)

@app.get("/", summary="Health Check / Root Endpoint")
def read_root():
    logger.info("Root health-check endpoint pinged.")
    return {"message": f"Welcome to {settings.PROJECT_NAME} API backend!"}
