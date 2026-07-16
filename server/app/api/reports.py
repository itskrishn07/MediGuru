import os
import logging
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database import crud
from database.schemas import DocumentResponse
from database.models import UserORM
from api.dependencies import get_current_user
from services.summary_service import summarize_document
from services.vector_service import delete_document_from_chroma

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("", response_model=List[DocumentResponse])
async def list_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    """
    Lists all reports belonging only to the authenticated user.
    """
    logger.info(f"Listing reports for user ID: {current_user.id}")
    documents = crud.get_user_documents(db, user_id=current_user.id, skip=skip, limit=limit)
    return documents

@router.get("/{report_id}", response_model=DocumentResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    """
    Retrieves a specific report only if it belongs to the authenticated user.
    """
    logger.info(f"Retrieving report {report_id} for user ID: {current_user.id}")
    document = crud.get_document_by_user(db, document_id=report_id, user_id=current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical report not found or access denied."
        )
    return document

@router.post("/{report_id}/summary")
async def summarize_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    """
    Generates a summary of a medical report only if it belongs to the authenticated user.
    """
    logger.info(f"Summarizing report {report_id} for user ID: {current_user.id}")
    document = crud.get_document_by_user(db, document_id=report_id, user_id=current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical report not found or access denied."
        )
    
    if not document.extracted_text:
        return {"report_id": report_id, "summary": "No extracted text available to summarize."}
        
    summary = summarize_document(document.extracted_text)
    return {"report_id": report_id, "summary": summary}

@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    """
    Deletes a medical report, its associated vector embeddings, and physical files from the system.
    Only allows the owner of the report to perform deletion.
    """
    logger.info(f"Delete request received for report ID {report_id} by user ID {current_user.id}")
    
    # 1. Verify existence and ownership
    document = crud.get_document_by_user(db, document_id=report_id, user_id=current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical report not found or access denied."
        )
        
    # 2. Delete physical file from the disk (if exists)
    if document.file_path:
        try:
            file_path = Path(document.file_path)
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                logger.info(f"Successfully deleted physical file: {document.file_path}")
        except Exception as file_err:
            logger.error(f"Failed to delete physical file {document.file_path}: {str(file_err)}")

    # 3. Clean up indexed embeddings from ChromaDB
    delete_document_from_chroma(document_id=report_id)

    # 4. Delete the document record and relations from PostgreSQL
    crud.delete_document(db, document_id=report_id)
    logger.info(f"Report ID {report_id} successfully deleted from PostgreSQL database.")

    return {"detail": f"Medical report {report_id} and all associated data successfully deleted."}
