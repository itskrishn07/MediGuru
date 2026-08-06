SUMMARY_PROMPT = (
    "Provide a clear, structured, and patient-friendly medical summary of the document below.\n"
    "Format the summary into distinct, easy-to-read sections without using markdown asterisks (** or *):\n"
    "• Patient & Doctor Info\n"
    "• Primary Condition / Diagnosis\n"
    "• Key Lab & Diagnostic Results\n"
    "• Prescribed Medications & Dosage\n"
    "• Follow-up Instructions & Recommendations\n\n"
    "Document Text:\n{document_text}"
)
