# Prompt templates for different medical extraction tasks

PRESCRIPTION_PROMPT = (
    "Extract structured medical information from the provided prescription, image, or medical document.\n\n"
    "Follow these strict instructions:\n"
    "- Never invent medicines. Only extract what is explicitly present in the document.\n"
    "- Return null for any field if the corresponding information is missing from the document.\n"
    "- Preserve medicine names exactly as written (including typos and OCR errors).\n"
    "- Don't normalize unknown abbreviations.\n"
    "- Return only valid JSON adhering to the specified schema.\n"
    "- Ignore logos, advertisements, and decorative text.\n"
    "- Assign a confidence score (float between 0.0 and 1.0) for each medicine entry, indicating your confidence in the correctness and accuracy of the extraction for that item."
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
