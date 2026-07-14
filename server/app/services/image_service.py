import base64
from pathlib import Path
from .ocr_service import run_ocr

def process_image(file_path: Path) -> str:
    """
    Processes an image file to extract text via OCR.
    """
    return run_ocr(file_path)

def get_image_base64(file_path: Path) -> str:
    """
    Encodes the image file to base64.
    """
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_image_mime_type(suffix: str) -> str:
    """
    Returns the appropriate MIME type for an image suffix.
    """
    suffix = suffix.lower()
    if suffix == ".png":
        return "image/png"
    elif suffix in (".jpg", ".jpeg"):
        return "image/jpeg"
    elif suffix == ".webp":
        return "image/webp"
    elif suffix == ".bmp":
        return "image/bmp"
    elif suffix in (".tiff", ".tif"):
        return "image/tiff"
    return "image/jpeg"  # default fallback
