from sqlalchemy.orm import Session
from .models import DocumentORM, MedicineORM
from .schemas import MedicalExtraction

def create_document(db: Session, filename: str, file_path: str, extracted_text: str | None, extraction: MedicalExtraction) -> DocumentORM:
    db_document = DocumentORM(
        filename=filename,
        file_path=file_path,
        extracted_text=extracted_text,
        patient_name=extraction.patient_name,
        doctor_name=extraction.doctor_name,
        diagnosis=extraction.diagnosis,
        lab_values=extraction.lab_values,
        follow_up_instructions=extraction.follow_up_instructions
    )
    db.add(db_document)
    db.flush()  # Populate db_document.id

    for med in extraction.medicines:
        db_medicine = MedicineORM(
            document_id=db_document.id,
            medicine_name=med.medicine_name,
            strength=med.strength,
            dosage=med.dosage,
            route=med.route,
            frequency=med.frequency,
            duration=med.duration,
            food_instruction=med.food_instruction,
            purpose=med.purpose,
            confidence=med.confidence
        )
        db.add(db_medicine)
    
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int) -> DocumentORM | None:
    return db.query(DocumentORM).filter(DocumentORM.id == document_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DocumentORM).offset(skip).limit(limit).all()
