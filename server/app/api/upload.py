import shutil
import logging
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from sqlalchemy.orm import Session

from core.config import settings
from database.database import get_db
from services.document_processor import process_document

router = APIRouter(prefix="/upload", tags=["Upload"])
logger = logging.getLogger(__name__)

UPLOAD_DIR = settings.UPLOAD_DIR
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Extract only the base name to prevent path traversal vulnerability
    filename = Path(file.filename).name
    if not filename or filename in (".", ".."):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    file_path = UPLOAD_DIR / filename
    
    # Save file in chunks to handle large files efficiently
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
    finally:
        await file.close()

    # Get file size
    file_size = file_path.stat().st_size

    # Orchestrate extraction and analysis
    result = process_document(db, file_path, file.content_type)

    return {
        "document_id": result.get("document_id"),
        "filename": file_path.name,
        "content_type": file.content_type,
        "size_bytes": file_size,
        "path": f"uploads/{file_path.name}",
        "extracted_text": result.get("extracted_text"),
        "extracted_data": result.get("extracted_data"),
        "indexed_in_chroma": result.get("indexed_in_chroma")
    }
