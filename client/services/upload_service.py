import logging
from typing import Tuple, Any
from services.api import APIService

logger = logging.getLogger(__name__)

class UploadService:
    """
    Handles file upload requests to backend endpoint:
    - POST /upload
    """

    @staticmethod
    def upload_document(file_name: str, file_bytes: bytes, content_type: str) -> Tuple[bool, Any]:
        """
        Sends document bytes to FastAPI /upload endpoint for OCR, extraction, and ChromaDB indexing.
        """
        logger.info(f"Uploading file {file_name} ({len(file_bytes)} bytes, content_type={content_type}) to backend...")
        return APIService.upload_file("upload", file_name, file_bytes, content_type)
