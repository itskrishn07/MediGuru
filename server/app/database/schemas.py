from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class Medicine(BaseModel):
    medicine_name: str = Field(description="Name of the medicine/drug as written in the document")
    strength: Optional[str] = Field(None, description="Strength of the medicine (e.g., 500mg, 10mg, 250mcg)")
    dosage: Optional[str] = Field(None, description="Dosage details (e.g., 1 tablet, 5ml, 2 drops)")
    route: Optional[str] = Field(None, description="Route of administration (e.g., Oral, Topical, Inhalation, IV)")
    frequency: Optional[str] = Field(None, description="Frequency of intake (e.g., twice daily, QD, every 8 hours)")
    duration: Optional[str] = Field(None, description="Duration of treatment (e.g., 5 days, 1 month)")
    food_instruction: Optional[str] = Field(None, description="Food instruction (e.g., before food, after food, with meals)")
    purpose: Optional[str] = Field(None, description="Purpose or indication of the medicine (e.g., for pain, for blood pressure)")
    confidence: Optional[float] = Field(None, description="Confidence score between 0.0 and 1.0 representing the accuracy of the extraction for this medicine")

    model_config = {
        "from_attributes": True
    }

class MedicalExtraction(BaseModel):
    patient_name: Optional[str] = Field(None, description="Name of the patient, if present")
    doctor_name: Optional[str] = Field(None, description="Name of the doctor/physician, if present")
    medicines: List[Medicine] = Field(default_factory=list, description="List of prescribed medicines with details")
    lab_values: Optional[str] = Field(None, description="Extracted lab values or test results (e.g., Blood Pressure, SpO2, glucose), if present")
    diagnosis: Optional[str] = Field(None, description="Diagnosis, symptoms, or medical condition mentioned")
    follow_up_instructions: Optional[str] = Field(None, description="Any follow-up details, instructions, next appointments, or advice")

    model_config = {
        "from_attributes": True
    }

class DocumentResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    filename: str
    file_path: str
    extracted_text: Optional[str] = None
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    diagnosis: Optional[str] = None
    lab_values: Optional[str] = None
    follow_up_instructions: Optional[str] = None
    created_at: datetime
    medicines: List[Medicine] = []

    model_config = {
        "from_attributes": True
    }

# --- Authentication & User Schemas ---
import re

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class UserCreate(BaseModel):
    email: str = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")
    full_name: str = Field(..., description="The user's full name")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        # Support common special characters
        special_chars = set("!@#$%^&*()-_=+[]{}|;:',.<>?/`~")
        if not any(char in special_chars for char in v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class LoginRequest(BaseModel):
    email: str = Field(..., description="The user's registered email address")
    password: str = Field(..., description="The user's password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.strip().lower()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

