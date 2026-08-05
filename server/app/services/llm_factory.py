import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from core.exceptions import MediGuruException

logger = logging.getLogger(__name__)

def get_gemini_llm(model_name: str = "gemini-2.5-flash", temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    Factory function to create and return a configured ChatGoogleGenerativeAI instance.
    """
    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        logger.error("Attempted LLM call without GEMINI_API_KEY or GOOGLE_API_KEY configured.")
        raise MediGuruException(
            message="LLM API key required. Please configure GEMINI_API_KEY or GOOGLE_API_KEY environment variable.",
            status_code=400
        )
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        api_key=api_key,
        timeout=60
    )
