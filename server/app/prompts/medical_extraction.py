# Prompt templates for medical document extraction and validation

PRESCRIPTION_PROMPT = (
    "Analyze the provided image or document and perform medical extraction.\n\n"
    "Step 1: Check if the document is medical-related (doctor prescription, lab report, discharge summary, clinical note, health bill).\n"
    "If the document is NOT medical-related (e.g. random photo, grocery receipt, invoice, landscape, book page, code snippet):\n"
    "- Set is_medical_document to false.\n"
    "- Set summary to 'The uploaded file does not appear to be a medical report, prescription, or health record. Please upload a valid medical document.'\n"
    "- Leave patient_name, doctor_name, diagnosis, lab_values, and medicines empty/null.\n\n"
    "Step 2: If the document IS medical-related:\n"
    "- Set is_medical_document to true.\n"
    "- Extract patient name, doctor name, diagnosis, lab results, follow-up instructions, and active medicines.\n"
    "- Never invent medicines or diagnoses. Extract only what is explicitly present.\n"
    "- Preserve medicine names exactly as written.\n"
    "- Provide a clear, patient-friendly summary."
)

LAB_REPORT_PROMPT = (
    "Extract structured lab results, reference ranges, and abnormal values from this laboratory report."
)

DISCHARGE_SUMMARY_PROMPT = (
    "Extract admission details, diagnosis, course in hospital, surgeries, and discharge instructions "
    "from this discharge summary."
)

QUESTION_ANSWER_PROMPT = (
    "Answer the patient's questions accurately based on the provided medical records and history."
)

PATIENT_SUMMARY_PROMPT = (
    "Generate a concise patient summary, highlighting active issues, current medications, and upcoming follow-ups."
)
