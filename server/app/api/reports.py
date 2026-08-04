import logging
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import DocumentResponse, SummaryResponse
from database.models import UserORM
from api.dependencies import get_current_user
from services.document_service import DocumentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get(
    "",
    response_model=List[DocumentResponse],
    status_code=status.HTTP_200_OK,
    summary="List medical reports",
    description="Lists all medical reports belonging only to the authenticated user."
)
async def list_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    logger.info(f"Listing reports for user ID: {current_user.id}")
    return DocumentService.get_user_reports(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get(
    "/{report_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get report details",
    description="Retrieves a specific medical report belonging only to the authenticated user."
)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    logger.info(f"Retrieving report {report_id} for user ID: {current_user.id}")
    return DocumentService.get_user_report_by_id(db=db, report_id=report_id, user_id=current_user.id)

@router.post(
    "/{report_id}/summary",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate medical report summary",
    description="Generates an AI summary of a medical report belonging only to the authenticated user."
)
async def summarize_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    logger.info(f"Summarizing report {report_id} for user ID: {current_user.id}")
    return DocumentService.summarize_user_report(db=db, report_id=report_id, user_id=current_user.id)

@router.delete(
    "/{report_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete medical report",
    description="Deletes a medical report, its associated vector embeddings, and physical files from the system."
)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    logger.info(f"Delete request received for report ID {report_id} by user ID {current_user.id}")
    return DocumentService.delete_user_report(db=db, report_id=report_id, user_id=current_user.id)
