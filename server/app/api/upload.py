import logging
from fastapi import APIRouter, File, UploadFile, status, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserORM
from database.schemas import UploadResponse
from api.dependencies import get_current_user
from services.document_service import DocumentService

router = APIRouter(prefix="/upload", tags=["Upload"])
logger = logging.getLogger(__name__)

@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload medical document",
    description="Uploads a medical document (Image or PDF), extracts text via OCR, parses medical data with Gemini LLM, saves to PostgreSQL, and indexes in ChromaDB."
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    return DocumentService.save_and_process_upload(db=db, file=file, current_user=current_user)
