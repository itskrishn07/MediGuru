from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from database.models import UserORM
from api.dependencies import get_current_user
from services.chat_service import chat_with_records

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str | None = Field(None, description="The medical query/question from the user")
    question: str | None = Field(None, description="Alternative field for the medical query")
    document_id: int | None = Field(None, description="Optional document ID to restrict context to")

@router.post("")
async def chat_endpoint(
    request: ChatRequest,
    current_user: UserORM = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = request.query or request.question
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query or question cannot be empty")
    
    # 1. Fetch user's documents to restrict scope
    user_docs = crud.get_user_documents(db, user_id=current_user.id)
    user_doc_ids = [d.id for d in user_docs]
    
    # 2. Check document ownership and determine scope
    if request.document_id is not None:
        if request.document_id not in user_doc_ids:
            raise HTTPException(status_code=404, detail="Medical report not found or access denied")
        allowed_ids = [request.document_id]
    else:
        allowed_ids = user_doc_ids
        
    # 3. If no documents exist, return gracefully without querying LLM
    if not allowed_ids:
        return {
            "query": query,
            "answer": "You do not have any uploaded medical reports. Please upload a report to start chatting."
        }
    
    answer = chat_with_records(query, document_ids=allowed_ids)
    return {"query": query, "answer": answer}
