import os
import logging
import time
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from database.schemas import MedicalExtraction
from prompts import PRESCRIPTION_PROMPT
from core.config import settings
from .image_service import get_image_base64, get_image_mime_type

_llm = None
_structured_llm = None

def get_llm():
    global _llm, _structured_llm
    if _structured_llm is None:
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("API key required for Gemini Developer API. Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
        
        _llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=api_key)
        _structured_llm = _llm.with_structured_output(MedicalExtraction)
    return _structured_llm

logger = logging.getLogger(__name__)

def analyze_medical_document(
    ocr_text: str | None,
    image_path: Path | None = None,
    suffix: str | None = None
) -> dict | None:
    """
    Invokes the Gemini model using LangChain to extract structured medical information.
    """
    # Ensure API keys are set before calling the LLM
    if not settings.GOOGLE_API_KEY:
        logger.warning("LLM processing skipped: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        return {
            "error": "LLM processing skipped: Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
        }
        
    prompt_text = PRESCRIPTION_PROMPT
    if ocr_text and not ocr_text.startswith("OCR Extraction Failed:"):
        prompt_text += f"\n\nHere is the OCR-extracted text from the document:\n{ocr_text}"
    
    content = [{"type": "text", "text": prompt_text}]

    # Pass base64 image if it's an image file to leverage vision model capabilities
    if image_path and suffix:
        try:
            base64_image = get_image_base64(image_path)
            mime_type = get_image_mime_type(suffix)
            
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}"
                }
            })
            logger.info("Multimodal input prepared: attached base64 image.")
        except Exception as img_err:
            logger.error(f"Failed to encode image to base64: {str(img_err)}")
            # Fallback to text-only prompt if base64 conversion fails
            pass

    # Invoke the structured LangChain model
    message = HumanMessage(content=content)
    logger.info("Gemini processing started (structured medical extraction)...")
    start_time = time.perf_counter()
    try:
        extraction_result = get_llm().invoke([message])
        latency = time.perf_counter() - start_time
        logger.info(f"Gemini processing finished successfully. Latency: {latency:.3f}s.")
        if extraction_result:
            return extraction_result.model_dump()
    except Exception as llm_err:
        latency = time.perf_counter() - start_time
        logger.error(f"Gemini processing failed after {latency:.3f}s. Error: {str(llm_err)}", exc_info=True)
        return {
            "error": f"LLM Processing Failed: {str(llm_err)}"
        }
    return None
