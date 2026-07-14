from fastapi import APIRouter, HTTPException, Query
from services.chat_service import chat_with_records

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("")
async def chat_endpoint(query: str = Query(..., description="The medical query/question from the user"), document_id: int | None = Query(None, description="Optional document ID to restrict context to")):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    answer = chat_with_records(query, document_id=document_id)
    return {"query": query, "answer": answer}
