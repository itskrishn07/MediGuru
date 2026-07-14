from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database import crud
from database.schemas import DocumentResponse
from services.summary_service import summarize_document

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("", response_model=List[DocumentResponse])
async def list_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents

@router.get("/{report_id}", response_model=DocumentResponse)
async def get_report(report_id: int, db: Session = Depends(get_db)):
    document = crud.get_document(db, report_id)
    if not document:
        raise HTTPException(status_code=404, detail="Medical report not found")
    return document

@router.post("/{report_id}/summary")
async def summarize_report(report_id: int, db: Session = Depends(get_db)):
    document = crud.get_document(db, report_id)
    if not document:
        raise HTTPException(status_code=404, detail="Medical report not found")
    
    if not document.extracted_text:
        return {"report_id": report_id, "summary": "No extracted text available to summarize."}
        
    summary = summarize_document(document.extracted_text)
    return {"report_id": report_id, "summary": summary}
