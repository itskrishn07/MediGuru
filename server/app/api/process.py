import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas import ProcessResponse
from services.document_processor import process_document
from core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Document Processing"])

@router.post("/process", response_model=ProcessResponse, summary="Process Medical Document")
def process_medical_document(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_document"
    logger.info(f"Received document processing request for file: {filename}")
    
    # Save file to temporary directory
    temp_file_path = settings.UPLOAD_DIR / filename
    try:
        content = file.file.read()
        if len(content) > settings.MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=400, detail=f"File size exceeds limit ({settings.MAX_FILE_SIZE_BYTES / (1024*1024):.1f}MB)")

        with open(temp_file_path, "wb") as f:
            f.write(content)
            
        logger.info(f"Saved temporary upload file to: {temp_file_path}")
    except HTTPException:
        raise
    except Exception as err:
        logger.error(f"Failed to save temporary upload: {str(err)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to handle file upload: {str(err)}")

    try:
        result = process_document(temp_file_path, file.content_type or "")
        return ProcessResponse(**result)
    except Exception as proc_err:
        logger.error(f"Document processing failed for {filename}: {str(proc_err)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(proc_err)}")
