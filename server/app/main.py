import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Add current directory to path to enable direct importing of local modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Initialize logging configuration
import core.logger  # noqa

from fastapi import FastAPI
from services.ocr_service import initialize_ocr
from database.database import engine, Base
from api.upload import router as upload_router
from api.chat import router as chat_router
from api.reports import router as reports_router
from api.auth import router as auth_router
from api.users import router as users_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize database tables
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as db_err:
        logger.error(f"Failed to initialize database tables: {str(db_err)}", exc_info=True)

    # 2. Pre-warm OCR models
    logger.info("Initializing PaddleOCR models on startup...")
    try:
        initialize_ocr()
        logger.info("PaddleOCR models successfully initialized on startup.")
    except Exception as e:
        logger.error(f"Failed to initialize PaddleOCR models on startup: {str(e)}", exc_info=True)
    yield

# Initialize the application instance
app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(reports_router)

# Define a root path operation
@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI application!"}
