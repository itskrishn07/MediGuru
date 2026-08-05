import logging
from fastapi import APIRouter
from schemas import SessionClearResponse
from vectorstore.chroma import reset_chroma_session

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Session Management"])

@router.post("/clear-session", response_model=SessionClearResponse, summary="Clear Active Session")
def clear_session_endpoint():
    logger.info("Session clear requested by client.")
    reset_chroma_session()
    return SessionClearResponse(
        message="Session cleared successfully. All temporary files and vector embeddings have been deleted."
    )
