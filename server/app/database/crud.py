from sqlalchemy.orm import Session
from .models import DocumentORM, MedicineORM, UserORM
from .schemas import MedicalExtraction, UserCreate

def create_document(db: Session, filename: str, file_path: str, extracted_text: str | None, extraction: MedicalExtraction, user_id: int) -> DocumentORM:
    db_document = DocumentORM(
        filename=filename,
        file_path=file_path,
        extracted_text=extracted_text,
        patient_name=extraction.patient_name,
        doctor_name=extraction.doctor_name,
        diagnosis=extraction.diagnosis,
        lab_values=extraction.lab_values,
        follow_up_instructions=extraction.follow_up_instructions,
        user_id=user_id
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

def get_document_by_user(db: Session, document_id: int, user_id: int) -> DocumentORM | None:
    return db.query(DocumentORM).filter(DocumentORM.id == document_id, DocumentORM.user_id == user_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DocumentORM).offset(skip).limit(limit).all()

def get_user_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(DocumentORM).filter(DocumentORM.user_id == user_id).offset(skip).limit(limit).all()

def delete_document(db: Session, document_id: int) -> bool:
    db_document = db.query(DocumentORM).filter(DocumentORM.id == document_id).first()
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False

# --- User CRUD ---

def get_user_by_email(db: Session, email: str) -> UserORM | None:
    return db.query(UserORM).filter(UserORM.email == email.strip().lower()).first()

def get_user_by_id(db: Session, user_id: int) -> UserORM | None:
    return db.query(UserORM).filter(UserORM.id == user_id).first()

def create_user(db: Session, user: UserCreate, hashed_password: str) -> UserORM:
    db_user = UserORM(
        email=user.email.strip().lower(),
        full_name=user.full_name,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

