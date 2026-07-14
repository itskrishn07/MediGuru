import logging
from pathlib import Path
from sqlalchemy.orm import Session

from .pdf_service import process_pdf
from .image_service import process_image
from .llm_service import analyze_medical_document
from .vector_service import index_document
from database import crud
from database.schemas import MedicalExtraction
from core.constants import SUPPORTED_IMAGE_EXTENSIONS, SUPPORTED_PDF_EXTENSIONS

logger = logging.getLogger(__name__)

def process_document(db: Session, file_path: Path, content_type: str) -> dict:
    """
    Orchestrates the entire document processing pipeline:
    1. Determines file type (PDF vs Image).
    2. Invokes correct extraction service (pdf_service / image_service) to perform text extraction/OCR.
    3. Invokes LLM service to perform structured medical data extraction.
    4. Saves the structured JSON results to PostgreSQL.
    5. Chunks, embeds, and indexes the text in ChromaDB.
    """
    suffix = file_path.suffix.lower()
    is_pdf = (content_type == "application/pdf") or (suffix in SUPPORTED_PDF_EXTENSIONS)
    is_image = (content_type and content_type.startswith("image/")) or (suffix in SUPPORTED_IMAGE_EXTENSIONS)

    extracted_text = None

    if is_pdf:
        try:
            logger.info(f"Routing document {file_path.name} to PDF service.")
            extracted_text = process_pdf(file_path)
        except Exception as ocr_err:
            logger.error(f"Failed to process PDF {file_path.name}: {str(ocr_err)}")
            extracted_text = f"OCR Extraction Failed: {str(ocr_err)}"
    elif is_image:
        try:
            logger.info(f"Routing document {file_path.name} to Image service.")
            extracted_text = process_image(file_path)
        except Exception as ocr_err:
            logger.error(f"Failed to process Image {file_path.name}: {str(ocr_err)}")
            extracted_text = f"OCR Extraction Failed: {str(ocr_err)}"

    # LLM Processing
    extracted_data = None
    db_document = None
    indexed_in_chroma = False

    if is_pdf or is_image:
        # Pass image_path only if it is an image to leverage vision model capabilities
        image_path = file_path if is_image else None
        extracted_data_dict = analyze_medical_document(
            ocr_text=extracted_text,
            image_path=image_path,
            suffix=suffix if is_image else None
        )
        
        # 1. Parse extraction result to MedicalExtraction schema
        if extracted_data_dict and "error" not in extracted_data_dict:
            try:
                extracted_data = MedicalExtraction(**extracted_data_dict)
            except Exception as schema_err:
                logger.error(f"Failed to parse extraction output to schema: {str(schema_err)}")
                extracted_data = MedicalExtraction()
        else:
            extracted_data = MedicalExtraction()

        # 2. Save structured extraction in PostgreSQL
        try:
            logger.info(f"Saving extracted document '{file_path.name}' to PostgreSQL...")
            db_document = crud.create_document(
                db=db,
                filename=file_path.name,
                file_path=str(file_path),
                extracted_text=extracted_text,
                extraction=extracted_data
            )
            logger.info(f"Successfully saved document in DB. ID: {db_document.id}")
        except Exception as db_err:
            logger.error(f"Failed to save document to PostgreSQL: {str(db_err)}", exc_info=True)

        # 3. Chunk and index text into ChromaDB using the PostgreSQL DB ID
        if db_document and extracted_text:
            logger.info(f"Indexing document '{file_path.name}' text in ChromaDB...")
            indexed_in_chroma = index_document(
                document_id=db_document.id,
                filename=file_path.name,
                text=extracted_text
            )

    return {
        "document_id": db_document.id if db_document else None,
        "filename": file_path.name,
        "content_type": content_type,
        "extracted_text": extracted_text,
        "extracted_data": extracted_data.model_dump() if extracted_data else None,
        "indexed_in_chroma": indexed_in_chroma
    }
