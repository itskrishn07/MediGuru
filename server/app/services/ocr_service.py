import logging
import time
from pathlib import Path
from paddleocr import PaddleOCR

logger = logging.getLogger("service.ocr")
_ocr = None

def get_ocr_instance() -> PaddleOCR:
    global _ocr
    if _ocr is None:
        logger.info("Initializing PaddleOCR instance (first-time model download/load)...")
        _ocr = PaddleOCR(use_angle_cls=True, lang="en", enable_mkldnn=False)
        logger.info("PaddleOCR instance initialized successfully.")
    return _ocr

def initialize_ocr() -> None:
    """
    Eagerly initializes the PaddleOCR instance (pre-warms the models).
    """
    logger.info("Pre-warming PaddleOCR models...")
    get_ocr_instance()
    logger.info("PaddleOCR pre-warming complete.")

def run_ocr(file_path: Path) -> str:
    """
    Performs OCR on the given file using PaddleOCR.
    """
    logger.info(f"Starting OCR processing for file: {file_path.name}")
    start_time = time.perf_counter()
    try:
        ocr_instance = get_ocr_instance()
        result = ocr_instance.ocr(str(file_path))
        
        text_lines = []
        if result:
            for item in result:
                if isinstance(item, dict):
                    texts = item.get("rec_texts", [])
                    for text in texts:
                        if isinstance(text, str):
                            text_lines.append(text)
                elif isinstance(item, list):
                    for line in item:
                        if line and len(line) > 1 and isinstance(line[1], tuple):
                            text_lines.append(line[1][0])
        
        extracted_text = "\n".join(text_lines)
        latency = time.perf_counter() - start_time
        logger.info(f"OCR finished for file: {file_path.name} in {latency:.3f}s. Extracted {len(text_lines)} text lines ({len(extracted_text)} chars).")
        return extracted_text
    except Exception as e:
        latency = time.perf_counter() - start_time
        logger.error(f"OCR failed for file: {file_path.name} after {latency:.3f}s: {str(e)}", exc_info=True)
        raise e
