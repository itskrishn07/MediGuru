from pydantic import BaseModel, Field
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
