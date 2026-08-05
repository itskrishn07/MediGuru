import logging
from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from services.chat_service import chat_with_records

logger = logging.getLogger(__name__)
router = APIRouter(tags=["RAG Chat"])

@router.post("/chat", response_model=ChatResponse, summary="RAG Chat Question Answering")
def chat_endpoint(request: ChatRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question prompt cannot be empty.")

    logger.info(f"Received RAG chat request: '{request.question}'")
    try:
        res = chat_with_records(request.question)
        return ChatResponse(**res)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")
