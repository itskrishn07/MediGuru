import logging
import pypdf
from pathlib import Path
from .ocr_service import run_ocr


logger = logging.getLogger(__name__)

def extract_native_text(file_path: Path) -> str:
    """
    Attempts to extract text natively from a PDF file using pypdf.
    """
        
    text_parts = []
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    return "\n".join(text_parts).strip()

def process_pdf(file_path: Path) -> str:
    """
    Processes a PDF file. Attempts native text extraction first.
    If no text is found (e.g. scanned PDF), falls back to OCR.
    """
    try:
        native_text = extract_native_text(file_path)
        if native_text:
            logger.info("Successfully extracted text natively from PDF.")
            return native_text
    except Exception as e:
        logger.error(f"Native PDF extraction failed: {str(e)}. Falling back to OCR.")
            
    logger.info("Falling back to OCR for PDF text extraction.")
    return run_ocr(file_path)
