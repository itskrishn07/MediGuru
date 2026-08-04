import logging
import pypdf
from pathlib import Path
from .ocr_service import run_ocr

logger = logging.getLogger("service.pdf")

def extract_native_text(file_path: Path) -> str:
    """
    Attempts to extract text natively from a PDF file using pypdf.
    """
    text_parts = []
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        num_pages = len(reader.pages)
        logger.info(f"Extracting native text from PDF '{file_path.name}' ({num_pages} pages)")
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_parts.append(text)

    extracted = "\n".join(text_parts).strip()
    logger.info(f"Native PDF extraction finished for '{file_path.name}'. Character count: {len(extracted)}")
    return extracted

def process_pdf(file_path: Path) -> str:
    """
    Processes a PDF file. Attempts native text extraction first.
    If no text is found (e.g. scanned PDF), falls back to OCR.
    """
    logger.info(f"Processing PDF document: {file_path.name}")
    try:
        native_text = extract_native_text(file_path)
        if native_text:
            logger.info(f"Native PDF text extraction successful for '{file_path.name}'. Skipping OCR.")
            return native_text
        else:
            logger.warning(f"No native text found in PDF '{file_path.name}'. PDF appears to be a scanned image.")
    except Exception as e:
        logger.error(f"Native PDF extraction failed for '{file_path.name}': {str(e)}. Triggering OCR fallback.", exc_info=True)

    logger.info(f"Triggering PaddleOCR fallback for PDF document '{file_path.name}'...")
    return run_ocr(file_path)
