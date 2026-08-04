import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from .models import DocumentORM, MedicineORM, UserORM
from .schemas import MedicalExtraction, UserCreate

logger = logging.getLogger("db.crud")

# --- Document & Medicine Data Access ---

def create_document(
    db: Session,
    filename: str,
    file_path: str,
    extracted_text: Optional[str],
    extraction: MedicalExtraction,
    user_id: int
) -> DocumentORM:
    """
    Creates a document record along with associated medicine records in a single atomic transaction.
    """
    logger.info(f"Creating database Document record for '{filename}' (User ID: {user_id})...")
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
    db.flush()

    med_count = len(extraction.medicines)
    logger.info(f"Document ID {db_document.id} created. Adding {med_count} associated medicine records...")

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
    logger.info(f"Database commit successful: Document ID {db_document.id} with {med_count} medicines.")
    return db_document

def get_document(db: Session, document_id: int) -> Optional[DocumentORM]:
    logger.debug(f"DB Query: Fetching Document ID {document_id}")
    return db.query(DocumentORM).filter(DocumentORM.id == document_id).first()

def get_document_by_user(db: Session, document_id: int, user_id: int) -> Optional[DocumentORM]:
    logger.debug(f"DB Query: Fetching Document ID {document_id} for User ID {user_id}")
    return db.query(DocumentORM).filter(DocumentORM.id == document_id, DocumentORM.user_id == user_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100) -> List[DocumentORM]:
    logger.debug(f"DB Query: Fetching documents (skip={skip}, limit={limit})")
    return db.query(DocumentORM).offset(skip).limit(limit).all()

def get_user_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[DocumentORM]:
    logger.debug(f"DB Query: Fetching documents for User ID {user_id} (skip={skip}, limit={limit})")
    return db.query(DocumentORM).filter(DocumentORM.user_id == user_id).offset(skip).limit(limit).all()

def delete_document(db: Session, document_id: int) -> bool:
    logger.info(f"DB Operation: Deleting Document ID {document_id}...")
    db_document = db.query(DocumentORM).filter(DocumentORM.id == document_id).first()
    if db_document:
        db.delete(db_document)
        db.commit()
        logger.info(f"DB Operation: Document ID {document_id} deleted successfully.")
        return True
    logger.warning(f"DB Operation: Document ID {document_id} not found for deletion.")
    return False

# --- User Data Access ---

def get_user_by_email(db: Session, email: str) -> Optional[UserORM]:
    logger.debug(f"DB Query: Fetching User by email: {email}")
    return db.query(UserORM).filter(UserORM.email == email.strip().lower()).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[UserORM]:
    logger.debug(f"DB Query: Fetching User by ID: {user_id}")
    return db.query(UserORM).filter(UserORM.id == user_id).first()

def create_user(db: Session, user: UserCreate, hashed_password: str) -> UserORM:
    logger.info(f"DB Operation: Creating new User record for email: {user.email}")
    db_user = UserORM(
        email=user.email.strip().lower(),
        full_name=user.full_name,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"DB Operation: User record created successfully with User ID {db_user.id}")
    return db_user
