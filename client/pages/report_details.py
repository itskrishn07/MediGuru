import json
import streamlit as st
from services.report_service import ReportService
from components.report_viewer import render_document_paper_viewer

def render_report_details_page() -> None:
    """
    Renders the split-view Report Details page featuring document paper preview on the left
    and extracted clinical intelligence, medicines, diagnosis, and RAG chat bar on the right.
    """
    report_id = st.session_state.get("selected_report_id")

    report_data = None
    if report_id:
        success, res = ReportService.get_report_by_id(report_id)
        if success and isinstance(res, dict):
            report_data = res

    col1, col2 = st.columns([6, 6])

    with col1:
        # Left Panel: Document Viewer
        filename = report_data.get("filename", "Lab_Results_JohnDoe_Oct23.pdf") if report_data else "Lab_Results_JohnDoe_Oct23.pdf"
        st.markdown(f"### 📄 {filename}")
        
        # Download JSON button
        if report_data:
            json_str = json.dumps(report_data, indent=2)
            st.download_button(
                label="📥 Download JSON Analysis",
                data=json_str,
                file_name=f"{filename}_analysis.json",
                mime="application/json"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        render_document_paper_viewer(report_data)

    with col2:
        # Right Panel: Clinical Intelligence
        patient_name = report_data.get("patient_name") if report_data and report_data.get("patient_name") else "John Doe"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <h1 style="font-size: 26px; font-weight: 800; color: #0F172A; margin: 0;">{patient_name}</h1>
                    <div style="font-size: 12px; color: #64748B; margin-top: 4px;">🏥 St. Jude Medical Center • 📅 Oct 24, 2023</div>
                </div>
                <span class="badge-success">✓ Analyzed</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        tabs = st.tabs(["Overview", "Diagnosis", "Medicines", "Lab Results", "AI Summary"])

        with tabs[0]: # Overview
            st.markdown(
                """
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
                    <div style="background: white; padding: 16px; border-radius: 16px; border: 1px solid #E2E8F0;">
                        <h4 style="font-size: 13px; font-weight: 800; margin: 0 0 12px 0;">Key Metrics</h4>
                        <div style="font-size: 12px; line-height: 2;">
                            <div style="background: #F8FAFC; padding: 6px 10px; border-radius: 8px; margin-bottom: 6px;">BMI: <strong>24.5 (Normal)</strong></div>
                            <div style="background: #FFE4E6; color: #BE123C; padding: 6px 10px; border-radius: 8px; margin-bottom: 6px;">WBC Count: <strong>12.5 (High)</strong></div>
                            <div style="background: #F8FAFC; padding: 6px 10px; border-radius: 8px;">BP: <strong>118/76 mmHg</strong></div>
                        </div>
                    </div>
                    <div style="background: white; padding: 16px; border-radius: 16px; border: 1px solid #E2E8F0;">
                        <h4 style="font-size: 13px; font-weight: 800; margin: 0 0 8px 0;">Doctor Notes</h4>
                        <p style="font-size: 12px; color: #475569; line-height: 1.5; margin: 0;">
                            Patient presents with mild fatigue and occasional shortness of breath. Recommended comprehensive blood work.
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # AI Overview Highlight
            st.markdown(
                """
                <div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <h4 style="font-size: 14px; font-weight: 800; margin: 0;">AI Analysis Overview</h4>
                        <span style="color: #10B981; font-size: 12px; font-weight: 700;">● AI Processing Complete</span>
                    </div>
                    <div style="background: #F8FAFC; padding: 14px; border-radius: 12px; border: 1px solid #F1F5F9; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: #0F172A;">Mild Leukocytosis</div>
                            <div style="font-size: 12px; color: #64748B;">Elevated white blood cells suggests potential infection.</div>
                        </div>
                        <span style="font-size: 12px; font-weight: 800; color: #0055D4; border-bottom: 2px solid #0055D4;">98% Match</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with tabs[1]: # Diagnosis
            diag_text = report_data.get("diagnosis") if report_data and report_data.get("diagnosis") else "Mild Leukocytosis secondary to early-stage respiratory tract infection. Patient reports mild fatigue."
            st.info(f"🩺 **Extracted Diagnosis:**\n\n{diag_text}")

        with tabs[2]: # Medicines
            st.markdown("### 💊 Prescribed Medicines")
            medicines = report_data.get("medicines", []) if report_data else []
            if not medicines:
                medicines = [
                    {"medicine_name": "Paracetamol 650mg", "dosage": "1 Tablet", "frequency": "Twice Daily", "duration": "5 Days", "food_instruction": "After Food"},
                    {"medicine_name": "Amoxicillin 500mg", "dosage": "1 Capsule", "frequency": "Every 8 Hours", "duration": "7 Days", "food_instruction": "With Water"}
                ]
            for med in medicines:
                mname = med.get("medicine_name", "Medicine")
                dos = med.get("dosage", "1 Tablet")
                freq = med.get("frequency", "Daily")
                dur = med.get("duration", "5 Days")
                food = med.get("food_instruction", "After Food")
                st.markdown(
                    f"""
                    <div style="padding: 12px; border-radius: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: #0F172A;">{mname}</div>
                            <div style="font-size: 12px; color: #64748B;">{dos} • {freq} • {dur}</div>
                        </div>
                        <span class="badge-success">{food}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with tabs[3]: # Lab Results
            st.markdown("### 🔬 Lab Results Parameter Data")
            lab_text = report_data.get("lab_values") if report_data and report_data.get("lab_values") else "White Blood Cells: 12.5 x10³/µL (High)\nHemoglobin: 14.2 g/dL (Normal)\nFasting Glucose: 98 mg/dL (Normal)"
            st.code(lab_text)

        with tabs[4]: # AI Summary
            summary_text = "The patient shows a mild elevation in white blood cell count (12.5 x10³/µL), indicating a mild immune response or low-grade infection. All metabolic markers remain within optimal baseline limits."
            st.success(f"📝 **AI Summary:**\n\n{summary_text}")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Interactive Chat Trigger Button
        if st.button("💬 Chat with this Medical Report", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Chat"
            st.rerun()
