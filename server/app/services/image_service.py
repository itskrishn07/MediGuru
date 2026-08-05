import logging
import base64
from pathlib import Path

logger = logging.getLogger("service.image")

def get_image_base64(file_path: Path) -> str:
    """
    Encodes the image file to base64 for Gemini Vision API.
    """
    logger.debug(f"Encoding image to base64: {file_path.name}")
    with open(file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        logger.debug(f"Base64 encoding complete for {file_path.name} (length: {len(encoded)})")
        return encoded

def get_image_mime_type(suffix: str) -> str:
    """
    Returns the appropriate MIME type for an image suffix.
    """
    suffix_lower = suffix.lower()
    mapping = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".tif": "image/tiff"
    }
    mime = mapping.get(suffix_lower, "image/jpeg")
    logger.debug(f"Resolved MIME type for suffix '{suffix}' -> {mime}")
    return mime
