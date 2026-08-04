import logging
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from database.models import UserORM
from database.schemas import ChatRequest, ChatResponse
from api.dependencies import get_current_user
from services.chat_service import chat_with_records

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)

@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with medical records",
    description="Answers user queries using Retrieval-Augmented Generation (RAG) over uploaded medical reports."
)
async def chat_endpoint(
    request: ChatRequest,
    current_user: UserORM = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = request.query or request.question
    if not query or not query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query or question cannot be empty"
        )
    
    # 1. Retrieve user's documents to establish ownership boundaries
    user_docs = crud.get_user_documents(db, user_id=current_user.id)
    user_doc_ids = [d.id for d in user_docs]
    
    if request.document_id is not None:
        if request.document_id not in user_doc_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical report not found or access denied"
            )
        allowed_ids = [request.document_id]
    else:
        allowed_ids = user_doc_ids
        
    if not allowed_ids:
        return ChatResponse(
            query=query,
            answer="You do not have any uploaded medical reports. Please upload a report to start chatting."
        )
    
    answer = chat_with_records(query, document_ids=allowed_ids)
    return ChatResponse(query=query, answer=answer)
