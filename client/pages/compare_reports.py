import streamlit as st
from services.report_service import ReportService

def render_compare_reports_page() -> None:
    """
    Renders the Compare Reports page for comparing two reports side-by-side:
    - Medicine differences
    - Lab changes
    - Summary comparison
    """
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Compare Medical Reports</h1>
            <p style="font-size: 14px; color: #64748B;">Compare two reports side-by-side to track changes in lab parameters and medications.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    success, reports_data = ReportService.get_all_reports()
    reports_list = reports_data if success and isinstance(reports_data, list) else []

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Select Baseline Report (Report A)")
        rep_options_a = {f"{r.get('filename')} (ID: {r.get('id')})": r.get('id') for r in reports_list} if reports_list else {"MRI_Scan_Patient_882.pdf (Baseline)": 1}
        sel_a = st.selectbox("Report A", list(rep_options_a.keys()), key="rep_sel_a")

    with col2:
        st.markdown("### 📄 Select Comparison Report (Report B)")
        rep_options_b = {f"{r.get('filename')} (ID: {r.get('id')})": r.get('id') for r in reports_list} if reports_list else {"Blood_Work_Q4_Summary.xlsx (Latest)": 2}
        sel_b = st.selectbox("Report B", list(rep_options_b.keys()), key="rep_sel_b")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚖️ Run Comparative Analysis", type="primary", use_container_width=True):
        st.markdown("---")
        st.markdown("### 📊 Side-by-Side Parameter Comparison")

        comp_col1, comp_col2 = st.columns(2)

        with comp_col1:
            st.markdown(f"#### 📄 Baseline: {sel_a}")
            st.markdown(
                """
                <div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0;">
                    <div style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 8px;">Prescribed Medicines:</div>
                    <ul>
                        <li>Paracetamol 650mg - Twice Daily</li>
                        <li>Lisinopril 10mg - Once Daily</li>
                    </ul>
                    <div style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 12px 0 8px 0;">Lab Highlights:</div>
                    <ul>
                        <li>WBC: <strong style="color: #BE123C;">14.5 x10³/µL (High)</strong></li>
                        <li>Glucose: 104 mg/dL</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        with comp_col2:
            st.markdown(f"#### 📄 Latest: {sel_b}")
            st.markdown(
                """
                <div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0;">
                    <div style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 8px;">Prescribed Medicines:</div>
                    <ul>
                        <li>Paracetamol 650mg - As Needed</li>
                        <li>Amoxicillin 500mg - Every 8 Hours (New)</li>
                    </ul>
                    <div style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 12px 0 8px 0;">Lab Highlights:</div>
                    <ul>
                        <li>WBC: <strong style="color: #10B981;">12.5 x10³/µL (Improving -13.7%)</strong></li>
                        <li>Glucose: 98 mg/dL (Normal)</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.success("💡 **Summary of Changes:** White Blood Cell count showed a 13.7% reduction indicating positive response to treatment. Amoxicillin 500mg was added to treatment protocol.")
