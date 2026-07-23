import logging
from typing import Tuple, Any, Dict
from services.api import APIService

logger = logging.getLogger(__name__)

class ChatService:
    """
    Handles RAG conversational chat requests to FastAPI backend endpoint:
    - POST /chat
    """

    @staticmethod
    def send_question(question: str, report_id: str = None) -> Tuple[bool, Any]:
        """
        Sends user query to backend /chat endpoint for ChromaDB RAG retrieval & Gemini answer synthesis.
        """
        payload = {"question": question}
        if report_id:
            payload["report_id"] = report_id
            
        logger.info(f"Sending RAG question to backend: {question}")
        return APIService.post("chat", payload)
