import logging
import time
from pathlib import Path
from paddleocr import PaddleOCR

logger = logging.getLogger(__name__)
_ocr = None

def get_ocr_instance() -> PaddleOCR:
    global _ocr
    if _ocr is None:
        logger.info("Initializing PaddleOCR instance (first-time model load)...")
        # Initialize PaddleOCR (models will be downloaded/loaded on first run)
        # use_angle_cls=True handles rotated text/orientation correction
        # enable_mkldnn=False bypasses PIR compilation bugs on CPU
        _ocr = PaddleOCR(use_angle_cls=True, lang="en", enable_mkldnn=False)
        logger.info("PaddleOCR instance initialized successfully.")
    return _ocr

def initialize_ocr() -> None:
    """
    Eagerly initializes the PaddleOCR instance (pre-warms the models).
    """
    get_ocr_instance()

def run_ocr(file_path: Path) -> str:
    """
    Performs OCR on the given file using PaddleOCR.
    """
    logger.info(f"OCR started for file: {file_path.name}")
    start_time = time.perf_counter()
    try:
        ocr_instance = get_ocr_instance()
        result = ocr_instance.ocr(str(file_path))
        
        text_lines = []
        if result:
            for item in result:
                if isinstance(item, dict):
                    # New format (PaddleOCR 3.4.0+ using PaddleX backend)
                    texts = item.get("rec_texts", [])
                    for text in texts:
                        if isinstance(text, str):
                            text_lines.append(text)
                elif isinstance(item, list):
                    # Old format (a list of bounding boxes and texts)
                    for line in item:
                        if line and len(line) > 1 and isinstance(line[1], tuple):
                            text_lines.append(line[1][0])
        
        extracted_text = "\n".join(text_lines)
        latency = time.perf_counter() - start_time
        logger.info(f"OCR finished successfully for file: {file_path.name}. Duration: {latency:.3f}s. Extracted {len(text_lines)} lines of text.")
        return extracted_text
    except Exception as e:
        latency = time.perf_counter() - start_time
        logger.error(f"OCR failed for file: {file_path.name} after {latency:.3f}s. Error: {str(e)}", exc_info=True)
        raise e
