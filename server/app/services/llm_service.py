import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any
from langchain_core.messages import HumanMessage
from schemas import MedicalExtraction
from prompts.medical_extraction import PRESCRIPTION_PROMPT
from core.config import settings
from .llm_factory import get_gemini_llm
from .image_service import get_image_base64, get_image_mime_type

logger = logging.getLogger(__name__)

def invoke_structured_vision(message: HumanMessage, model_name: str = "gemini-2.5-flash") -> Optional[MedicalExtraction]:
    """
    Invokes Gemini with structured output mapping to MedicalExtraction.
    """
    llm = get_gemini_llm(model_name=model_name, temperature=0.0)
    structured_llm = llm.with_structured_output(MedicalExtraction)
    return structured_llm.invoke([message])

def analyze_medical_document(
    ocr_text: Optional[str],
    image_path: Optional[Path] = None,
    suffix: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Invokes Gemini to extract structured medical information & summary in ONE single call.
    Includes fallback to gemini-1.5-flash on rate limits (429).
    """
    if not settings.GOOGLE_API_KEY:
        logger.warning("LLM processing skipped: GEMINI_API_KEY environment variable is not set.")
        return {"error": "Please configure your GEMINI_API_KEY in server/app/.env file."}

    prompt_text = PRESCRIPTION_PROMPT
    if ocr_text and not ocr_text.startswith("OCR Extraction Failed:"):
        prompt_text += f"\n\nHere is the text from the document:\n{ocr_text}"

    content = [{"type": "text", "text": prompt_text}]

    if image_path and suffix:
        try:
            base64_image = get_image_base64(image_path)
            mime_type = get_image_mime_type(suffix)
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
            })
            logger.info("Multimodal vision input prepared: base64 image attached.")
        except Exception as img_err:
            logger.error(f"Failed to encode image to base64: {str(img_err)}")

    message = HumanMessage(content=content)
    logger.info("Gemini processing started (structured medical extraction + summary)...")
    start_time = time.perf_counter()
    
    # Primary Model Attempt: gemini-2.5-flash
    try:
        extraction_result = invoke_structured_vision(message, model_name="gemini-2.5-flash")
        latency = time.perf_counter() - start_time
        logger.info(f"Gemini 2.5 Flash analysis finished in {latency:.3f}s.")
        if extraction_result:
            return extraction_result.model_dump()
    except Exception as err1:
        err_str = str(err1)
        logger.warning(f"Primary model (gemini-2.5-flash) notice: {err_str}")
        
        # Fallback Model Attempt: gemini-1.5-flash if 429 rate limit or quota error
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Quota" in err_str:
            logger.info("Rate limit hit on gemini-2.5-flash. Falling back to gemini-1.5-flash...")
            try:
                fallback_result = invoke_structured_vision(message, model_name="gemini-1.5-flash")
                latency = time.perf_counter() - start_time
                logger.info(f"Fallback gemini-1.5-flash analysis finished in {latency:.3f}s.")
                if fallback_result:
                    return fallback_result.model_dump()
            except Exception as err2:
                logger.error(f"Fallback model also failed: {err2}")
                return {
                    "error": "Gemini API free tier rate limit reached. Please wait ~30 seconds and try again."
                }
        else:
            return {"error": f"Medical Analysis Notice: {err_str}"}

    return None
