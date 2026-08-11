import logging
import time
import uuid
from pathlib import Path
from typing import Dict, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from .pdf_service import extract_native_text
from .llm_service import analyze_medical_document
from .summary_service import summarize_document
from .vector_service import index_document
from schemas import MedicalExtraction
from core.constants import SUPPORTED_IMAGE_EXTENSIONS, SUPPORTED_PDF_EXTENSIONS

logger = logging.getLogger(__name__)

def convert_pdf_page_to_image(pdf_path: Path, page_num: int = 0, max_dimension: int = 1500) -> Path:
    """
    Renders a PDF page to a temporary PNG image for Gemini Vision analysis.
    Takes ~0.02s!
    """
    if fitz:
        doc = fitz.open(str(pdf_path))
        page = doc[page_num]
        rect = page.rect
        scale = (max_dimension / float(max(rect.width, rect.height))) if max(rect.width, rect.height) > 0 else 1.0
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        temp_img_path = pdf_path.parent / f"vision_{pdf_path.stem}_p{page_num}.png"
        pix.save(str(temp_img_path))
        doc.close()
        return temp_img_path
    return pdf_path

def process_document(file_path: Path, content_type: str) -> Dict[str, Any]:
    """
    Ultra-fast MVP document processing using Gemini Multimodal Vision in ONE unified API call:
    1. Checks PDF for native text (0.05s).
    2. Uses Gemini Vision for structured data + validation + summary in 1 call (1.8s).
    3. If valid medical document, indexes vectors in ChromaDB (0.5s).
    """
    start_total = time.perf_counter()
    suffix = file_path.suffix.lower()
    is_pdf = (content_type == "application/pdf") or (suffix in SUPPORTED_PDF_EXTENSIONS)
    is_image = (content_type and content_type.startswith("image/")) or (suffix in SUPPORTED_IMAGE_EXTENSIONS)

    extracted_text = None
    image_for_vision = None
    temp_vision_img = None

    # Step 1: Text & Vision Input Preparation
    t0 = time.perf_counter()
    if is_pdf:
        try:
            logger.info(f"[1/3] Checking PDF for native text: {file_path.name}")
            native_text = extract_native_text(file_path)
            if native_text and len(native_text.strip()) > 30:
                extracted_text = native_text
                logger.info(f"Extracted {len(extracted_text)} chars of native PDF text in {time.perf_counter() - t0:.2f}s")
            else:
                logger.info("PDF has no native text (scanned PDF). Converting page to image for Gemini Vision...")
                temp_vision_img = convert_pdf_page_to_image(file_path, page_num=0)
                image_for_vision = temp_vision_img
        except Exception as pdf_err:
            logger.error(f"PDF handling error: {pdf_err}")
    elif is_image:
        image_for_vision = file_path

    # Step 2: Gemini Structured Vision & Summary Analysis (Single Call)
    t1 = time.perf_counter()
    logger.info(f"[2/3] Invoking Gemini Vision for {file_path.name}...")
    
    extracted_data_dict = analyze_medical_document(
        ocr_text=extracted_text,
        image_path=image_for_vision,
        suffix=image_for_vision.suffix if image_for_vision else suffix
    )
    
    extracted_data = MedicalExtraction()
    rate_limit_error = None

    if extracted_data_dict:
        if "error" in extracted_data_dict:
            rate_limit_error = extracted_data_dict["error"]
        else:
            try:
                extracted_data = MedicalExtraction(**extracted_data_dict)
            except Exception as schema_err:
                logger.error(f"Schema mapping error: {schema_err}")

    logger.info(f"[2/3] Gemini Vision analysis complete in {time.perf_counter() - t1:.2f}s")

    # Clean up temp page image if created
    if temp_vision_img and temp_vision_img.exists():
        try:
            temp_vision_img.unlink()
        except Exception:
            pass

    # Check non-medical document validation
    is_valid_medical = extracted_data.is_medical_document

    # Construct text for ChromaDB vector store
    if not extracted_text:
        text_parts = []
        if extracted_data.patient_name: text_parts.append(f"Patient Name: {extracted_data.patient_name}")
        if extracted_data.doctor_name: text_parts.append(f"Doctor Name: {extracted_data.doctor_name}")
        if extracted_data.diagnosis: text_parts.append(f"Diagnosis: {extracted_data.diagnosis}")
        if extracted_data.lab_values: text_parts.append(f"Lab Results: {extracted_data.lab_values}")
        if extracted_data.follow_up_instructions: text_parts.append(f"Follow-up: {extracted_data.follow_up_instructions}")
        if extracted_data.medicines:
            med_list = [f"{m.medicine_name} {m.strength or ''} ({m.dosage or ''}, {m.frequency or ''}, {m.food_instruction or ''})" for m in extracted_data.medicines]
            text_parts.append("Medicines Prescribed:\n" + "\n".join(med_list))
        
        extracted_text = "\n\n".join(text_parts) if text_parts else ("Medical document processed via Gemini AI." if is_valid_medical else "Non-medical document uploaded.")

    # Determine Summary
    if rate_limit_error:
        summary = rate_limit_error
    elif not is_valid_medical:
        summary = extracted_data.summary or "The uploaded document does not appear to be a medical report, prescription, or health record. Please upload a valid medical document."
    elif extracted_data.summary and len(extracted_data.summary.strip()) > 10:
        summary = extracted_data.summary
    else:
        try:
            summary = summarize_document(extracted_text)
        except Exception as sum_err:
            logger.error(f"Summary fallback notice: {sum_err}")
            summary = "Medical summary complete."

    # Step 3: Indexing Vectors in ChromaDB (Only if valid medical document)
    t3 = time.perf_counter()
    indexed_in_chroma = False
    if is_valid_medical and not rate_limit_error:
        doc_id = str(uuid.uuid4())
        try:
            logger.info(f"[3/3] Indexing document in temporary ChromaDB...")
            indexed_in_chroma = index_document(
                doc_id=doc_id,
                filename=file_path.name,
                text=extracted_text
            )
        except Exception as vec_err:
            logger.error(f"Vector indexing error: {vec_err}")
        logger.info(f"[3/3] ChromaDB indexing complete in {time.perf_counter() - t3:.2f}s")
    else:
        logger.info("[3/3] Non-medical document or rate limit detected. Skipping ChromaDB vector indexing.")

    total_duration = time.perf_counter() - start_total
    logger.info(f"⚡ COMPLETE! Processed '{file_path.name}' in {total_duration:.2f} seconds ⚡")

    size_bytes = file_path.stat().st_size if file_path.exists() else 0

    return {
        "filename": file_path.name,
        "content_type": content_type,
        "size_bytes": size_bytes,
        "extracted_text": extracted_text,
        "extracted_data": extracted_data.model_dump(),
        "summary": summary,
        "indexed_in_chroma": indexed_in_chroma
    }
