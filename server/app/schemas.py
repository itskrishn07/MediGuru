from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class Medicine(BaseModel):
    medicine_name: str = Field(description="Name of the medicine/drug as written in the document")
    strength: Optional[str] = Field(None, description="Strength of the medicine (e.g., 500mg, 10mg)")
    dosage: Optional[str] = Field(None, description="Dosage details (e.g., 1 tablet, 5ml)")
    route: Optional[str] = Field(None, description="Route of administration (e.g., Oral, Topical)")
    frequency: Optional[str] = Field(None, description="Frequency of intake (e.g., twice daily, every 8 hours)")
    duration: Optional[str] = Field(None, description="Duration of treatment (e.g., 5 days, 1 month)")
    food_instruction: Optional[str] = Field(None, description="Food instruction (e.g., before food, after food)")
    purpose: Optional[str] = Field(None, description="Purpose or indication (e.g., for pain, for hypertension)")
    confidence: Optional[float] = Field(None, description="Confidence score between 0.0 and 1.0")

    model_config = ConfigDict(from_attributes=True)

class MedicalExtraction(BaseModel):
    patient_name: Optional[str] = Field(None, description="Name of the patient, if present")
    doctor_name: Optional[str] = Field(None, description="Name of the doctor/physician, if present")
    medicines: List[Medicine] = Field(default_factory=list, description="List of prescribed medicines with details")
    lab_values: Optional[str] = Field(None, description="Extracted lab values or test results")
    diagnosis: Optional[str] = Field(None, description="Diagnosis, symptoms, or medical condition mentioned")
    follow_up_instructions: Optional[str] = Field(None, description="Follow-up details or next appointments")

    model_config = ConfigDict(from_attributes=True)

class ProcessResponse(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size_bytes: int
    extracted_text: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    indexed_in_chroma: bool = False

class ChatRequest(BaseModel):
    question: str = Field(..., description="The medical question or query from the user")

class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: List[str] = []

class SessionClearResponse(BaseModel):
    message: str
