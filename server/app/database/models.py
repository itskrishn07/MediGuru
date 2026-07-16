from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    documents = relationship("DocumentORM", back_populates="user", cascade="all, delete-orphan")

class DocumentORM(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    patient_name = Column(String, nullable=True)
    doctor_name = Column(String, nullable=True)
    diagnosis = Column(Text, nullable=True)
    lab_values = Column(Text, nullable=True)
    follow_up_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("UserORM", back_populates="documents")
    medicines = relationship("MedicineORM", back_populates="document", cascade="all, delete-orphan")

class MedicineORM(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    medicine_name = Column(String, nullable=False)
    strength = Column(String, nullable=True)
    dosage = Column(String, nullable=True)
    route = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    food_instruction = Column(String, nullable=True)
    purpose = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)

    document = relationship("DocumentORM", back_populates="medicines")
