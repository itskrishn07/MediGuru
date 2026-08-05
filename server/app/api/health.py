from fastapi import APIRouter
from core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", summary="Health Check")
def health_check():
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0-mvp"
    }
