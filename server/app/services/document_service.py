import shutil
import logging
from pathlib import Path
from typing import List
from sqlalchemy.orm import Session
from fastapi import UploadFile

from core.config import settings
from core.exceptions import ResourceNotFoundError, MediGuruException
from database import crud
from database.models import UserORM, DocumentORM
from database.schemas import DocumentResponse, UploadResponse, SummaryResponse
from services.document_processor import process_document
from services.summary_service import summarize_document
from services.vector_service import delete_document_from_chroma

logger = logging.getLogger("service.document")

class DocumentService:
    @staticmethod
    def save_and_process_upload(
        db: Session,
        file: UploadFile,
        current_user: UserORM
    ) -> UploadResponse:
        """
        Saves uploaded file securely to disk, runs OCR & LLM processing, saves DB records, and indexes in ChromaDB.
        """
        filename = Path(file.filename).name if file.filename else ""
        if not filename or filename in (".", ".."):
            logger.warning(f"File upload rejected: Invalid filename '{file.filename}' for user ID {current_user.id}")
            raise MediGuruException(message="Invalid filename", status_code=400)

        upload_dir = settings.UPLOAD_DIR
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / filename

        logger.info(f"Processing file upload '{filename}' ({file.content_type}) for user ID {current_user.id}")

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_size = file_path.stat().st_size
            logger.info(f"Successfully saved physical file to disk: {file_path} ({file_size} bytes)")
        except Exception as e:
            logger.error(f"Failed to save uploaded file {filename} to disk: {str(e)}", exc_info=True)
            raise MediGuruException(message=f"Could not save file: {str(e)}", status_code=500)

        result = process_document(db, file_path, file.content_type or "", user_id=current_user.id)
        logger.info(f"Document processing completed for '{filename}'. Document ID: {result.get('document_id')}")

        return UploadResponse(
            document_id=result.get("document_id"),
            filename=file_path.name,
            content_type=file.content_type,
            size_bytes=file_size,
            path=f"uploads/{file_path.name}",
            extracted_text=result.get("extracted_text"),
            extracted_data=result.get("extracted_data"),
            indexed_in_chroma=result.get("indexed_in_chroma", False)
        )

    @staticmethod
    def get_user_reports(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[DocumentORM]:
        """
        Retrieves medical reports belonging to the user.
        """
        logger.info(f"Fetching medical reports list for user ID {user_id} (skip={skip}, limit={limit})")
        reports = crud.get_user_documents(db, user_id=user_id, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(reports)} medical reports for user ID {user_id}")
        return reports

    @staticmethod
    def get_user_report_by_id(db: Session, report_id: int, user_id: int) -> DocumentORM:
        """
        Retrieves a specific report belonging to the user or raises ResourceNotFoundError.
        """
        logger.info(f"Retrieving report ID {report_id} for user ID {user_id}")
        document = crud.get_document_by_user(db, document_id=report_id, user_id=user_id)
        if not document:
            logger.warning(f"Report retrieval failed: Report ID {report_id} not found or access denied for user ID {user_id}")
            raise ResourceNotFoundError(message="Medical report not found or access denied.")
        return document

    @staticmethod
    def summarize_user_report(db: Session, report_id: int, user_id: int) -> SummaryResponse:
        """
        Generates summary for a specific user report.
        """
        logger.info(f"Summary request received for report ID {report_id} by user ID {user_id}")
        document = DocumentService.get_user_report_by_id(db, report_id=report_id, user_id=user_id)
        if not document.extracted_text:
            logger.warning(f"Report ID {report_id} has no extracted text available to summarize.")
            return SummaryResponse(report_id=report_id, summary="No extracted text available to summarize.")

        summary_text = summarize_document(document.extracted_text)
        logger.info(f"Successfully generated summary for report ID {report_id}")
        return SummaryResponse(report_id=report_id, summary=summary_text)

    @staticmethod
    def delete_user_report(db: Session, report_id: int, user_id: int) -> dict:
        """
        Deletes report physical file, ChromaDB embeddings, and database records cleanly.
        """
        logger.info(f"Initiating deletion of report ID {report_id} for user ID {user_id}")
        document = DocumentService.get_user_report_by_id(db, report_id=report_id, user_id=user_id)

        # 1. Delete physical file
        if document.file_path:
            try:
                p_file = Path(document.file_path)
                if p_file.exists() and p_file.is_file():
                    p_file.unlink()
                    logger.info(f"Deleted physical file from disk: {document.file_path}")
            except Exception as file_err:
                logger.error(f"Failed to delete physical file {document.file_path}: {str(file_err)}", exc_info=True)

        # 2. Delete ChromaDB vector embeddings
        delete_document_from_chroma(document_id=report_id)

        # 3. Delete database record
        crud.delete_document(db, document_id=report_id)
        logger.info(f"Report ID {report_id} and all associated data successfully deleted for user ID {user_id}")

        return {"detail": f"Medical report {report_id} and all associated data successfully deleted."}
