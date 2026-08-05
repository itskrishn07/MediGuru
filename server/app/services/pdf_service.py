import logging
from pathlib import Path
import pypdf

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

logger = logging.getLogger("service.pdf")

def extract_native_text(file_path: Path) -> str:
    """
    Extracts text natively from a digital PDF file using PyMuPDF (fitz) or pypdf.
    Extremely fast (~0.01 seconds).
    """
    text_parts = []
    
    # 1. Try PyMuPDF first (fastest & most accurate)
    if fitz:
        try:
            doc = fitz.open(str(file_path))
            for page in doc:
                text = page.get_text()
                if text and len(text.strip()) > 10:
                    text_parts.append(text.strip())
            doc.close()
            if text_parts:
                extracted = "\n\n".join(text_parts).strip()
                logger.info(f"PyMuPDF extracted {len(extracted)} chars from '{file_path.name}'.")
                return extracted
        except Exception as err:
            logger.warning(f"PyMuPDF text extraction notice: {err}")

    # 2. Fallback to pypdf
    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text and len(text.strip()) > 10:
                    text_parts.append(text.strip())
        extracted = "\n\n".join(text_parts).strip()
        logger.info(f"pypdf extracted {len(extracted)} chars from '{file_path.name}'.")
        return extracted
    except Exception as e:
        logger.error(f"Native PDF extraction failed for '{file_path.name}': {str(e)}")

    return ""
