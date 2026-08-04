import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any
from langchain_core.messages import HumanMessage
from database.schemas import MedicalExtraction
from prompts import PRESCRIPTION_PROMPT
from core.config import settings
from .llm_factory import get_gemini_llm
from .image_service import get_image_base64, get_image_mime_type

logger = logging.getLogger(__name__)

_structured_llm = None

def get_structured_llm():
    global _structured_llm
    if _structured_llm is None:
        base_llm = get_gemini_llm(model_name="gemini-2.5-flash", temperature=0.0)
        _structured_llm = base_llm.with_structured_output(MedicalExtraction)
    return _structured_llm

def analyze_medical_document(
    ocr_text: Optional[str],
    image_path: Optional[Path] = None,
    suffix: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Invokes Gemini to extract structured medical information from text and/or images.
    """
    if not settings.GOOGLE_API_KEY:
        logger.warning("LLM processing skipped: GEMINI_API_KEY environment variable is not set.")
        return {"error": "LLM processing skipped: Please set GEMINI_API_KEY environment variable."}

    prompt_text = PRESCRIPTION_PROMPT
    if ocr_text and not ocr_text.startswith("OCR Extraction Failed:"):
        prompt_text += f"\n\nHere is the OCR-extracted text from the document:\n{ocr_text}"

    content = [{"type": "text", "text": prompt_text}]

    # Attach base64 image if available for multimodal processing
    if image_path and suffix:
        try:
            base64_image = get_image_base64(image_path)
            mime_type = get_image_mime_type(suffix)
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
            })
            logger.info("Multimodal input prepared: attached base64 image.")
        except Exception as img_err:
            logger.error(f"Failed to encode image to base64: {str(img_err)}")

    message = HumanMessage(content=content)
    logger.info("Gemini processing started (structured medical extraction)...")
    start_time = time.perf_counter()
    
    try:
        extraction_result = get_structured_llm().invoke([message])
        latency = time.perf_counter() - start_time
        logger.info(f"Gemini processing finished successfully in {latency:.3f}s.")
        if extraction_result:
            return extraction_result.model_dump()
    except Exception as llm_err:
        latency = time.perf_counter() - start_time
        logger.error(f"Gemini processing failed after {latency:.3f}s: {str(llm_err)}", exc_info=True)
        return {"error": f"LLM Processing Failed: {str(llm_err)}"}
        
    return None
