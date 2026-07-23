import streamlit as st
from typing import Dict, Any, Optional

def render_document_paper_viewer(report_data: Optional[Dict[str, Any]] = None) -> None:
    """
    Renders a styled medical document paper view matching the user's design screenshot.
    """
    patient_name = report_data.get("patient_name") if report_data and report_data.get("patient_name") else "John Doe"
    doctor_name = report_data.get("doctor_name") if report_data and report_data.get("doctor_name") else "Dr. Sarah Mitchell"
    diagnosis = report_data.get("diagnosis") if report_data and report_data.get("diagnosis") else "Mild Leukocytosis"
    
    st.markdown(
        f"""
        <div class="document-paper">
            <!-- Hospital Header -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #F1F5F9; padding-bottom: 16px; margin-bottom: 16px;">
                <div>
                    <h2 style="font-size: 22px; font-weight: 800; color: #0F172A; margin: 0;">St. Jude Medical Center</h2>
                    <p style="font-size: 12px; color: #64748B; margin: 2px 0 0 0;">Laboratory Analysis Department</p>
                </div>
                <div style="text-align: right; font-size: 11px; color: #64748B; font-weight: 600;">
                    <div>Case ID: <strong style="color: #0F172A;">#88321-JD</strong></div>
                    <div>Date: <strong style="color: #0F172A;">10/24/2023</strong></div>
                </div>
            </div>

            <div style="height: 3px; background-color: #0055D4; border-radius: 9999px; margin-bottom: 20px;"></div>

            <!-- Patient Metadata Box -->
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 20px; font-size: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                <div><span style="color: #64748B;">Patient:</span> <strong style="color: #0F172A;">{patient_name}</strong></div>
                <div><span style="color: #64748B;">DOB:</span> <strong style="color: #0F172A;">05/12/1985</strong></div>
                <div><span style="color: #64748B;">Physician:</span> <strong style="color: #0F172A;">{doctor_name}</strong></div>
                <div><span style="color: #64748B;">Sample Type:</span> <strong style="color: #0F172A;">Serum/Plasma</strong></div>
            </div>

            <!-- Hematology Results -->
            <div style="margin-bottom: 20px;">
                <h4 style="font-size: 12px; font-weight: 800; color: #0F172A; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 10px;">Hematology Results</h4>
                <div style="font-size: 12px; line-height: 2;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #F1F5F9;">
                        <span>Hemoglobin (Hb)</span><strong>14.2 g/dL</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #F1F5F9;">
                        <span>White Blood Cell Count</span><strong style="color: #BE123C;">12.5 x10³/µL ↑</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #F1F5F9;">
                        <span>Platelet Count</span><strong>250 x10³/µL</strong>
                    </div>
                </div>
            </div>

            <!-- Metabolic Panel -->
            <div>
                <h4 style="font-size: 12px; font-weight: 800; color: #0F172A; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 10px;">Metabolic Panel</h4>
                <div style="font-size: 12px; line-height: 2;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #F1F5F9;">
                        <span>Glucose, Fasting</span><strong>98 mg/dL</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #F1F5F9;">
                        <span>Creatinine</span><strong>0.9 mg/dL</strong>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
