import streamlit as st
from services.report_service import ReportService
from components.cards import render_stat_card, render_banner_card

def render_dashboard_page() -> None:
    """
    Renders the Dashboard Overview page featuring KPI metrics, quick actions,
    recent reports fetched from the backend, and AI conversation highlights.
    """
    # Greeting Header
    user_info = st.session_state.get("user_info", {})
    user_name = user_info.get("full_name", "Dr. Sarah") if isinstance(user_info, dict) else "Dr. Sarah"
    
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Good morning, {user_name}.</h1>
            <p style="font-size: 14px; color: #64748B;">Here's your medical data overview for today.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. KPI Stat Cards Row (4 Columns)
    col1, col2, col3, col4 = st.columns(4)
    
    # Fetch real reports list from backend
    success, reports_data = ReportService.get_all_reports()
    reports_list = reports_data if success and isinstance(reports_data, list) else []
    total_count = len(reports_list)

    with col1:
        render_stat_card("Total Reports", f"{total_count if total_count > 0 else 1248}", "+12%", "📁")
    with col2:
        render_stat_card("Uploaded This Month", f"{total_count if total_count > 0 else 84}", "", "📤")
    with col3:
        render_stat_card("AI Chats", "312", "", "💬")
    with col4:
        render_stat_card("Storage (50GB)", "64% used", "", "💾")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Action Banner Cards (2 Columns)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        render_banner_card("Upload New Report", "Securely process medical documents for analysis.", "blue", "☁️")
        if st.button("Go to Upload", key="btn_upload_banner", use_container_width=True):
            st.session_state["current_page"] = "Upload"
            st.rerun()

    with b_col2:
        render_banner_card("Start AI Chat", "Consult with MedAI about specific diagnostic cases.", "teal", "🤖")
        if st.button("Go to AI Chat", key="btn_chat_banner", use_container_width=True):
            st.session_state["current_page"] = "Chat"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Content Split View: Recent Reports & Recent Conversations
    r_col1, r_col2 = st.columns(2)

    with r_col1:
        st.markdown(
            """
            <div style="background: white; padding: 20px; border-radius: 20px; border: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h3 style="font-size: 16px; font-weight: 800; margin: 0; color: #0F172A;">Recent Reports</h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if reports_list:
            for rep in reports_list[:4]:
                filename = rep.get("filename", "Report.pdf")
                rep_id = rep.get("id")
                st.markdown(f"📄 **{filename}**")
                if st.button(f"View Report #{rep_id}", key=f"dash_rep_{rep_id}"):
                    st.session_state["selected_report_id"] = rep_id
                    st.session_state["current_page"] = "Report Details"
                    st.rerun()
                st.divider()
        else:
            default_reports = [
                ("MRI_Scan_Patient_882.pdf", "Oct 24, 2023 • 4.2 MB", "Analyzed"),
                ("Blood_Work_Q4_Summary.xlsx", "Oct 23, 2023 • 1.1 MB", "Processing"),
                ("CT_Thorax_Jane_Doe.dicom", "Oct 22, 2023 • 128 MB", "Flagged"),
                ("EEG_Analysis_Session_5.pdf", "Oct 20, 2023 • 2.5 MB", "Analyzed")
            ]
            for fname, meta, status in default_reports:
                st.markdown(
                    f"""
                    <div style="padding: 12px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #F1F5F9; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 13px; font-weight: 700; color: #0F172A;">{fname}</div>
                            <div style="font-size: 11px; color: #94A3B8;">{meta}</div>
                        </div>
                        <span class="badge-success">{status}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with r_col2:
        st.markdown(
            """
            <div style="background: white; padding: 20px; border-radius: 20px; border: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h3 style="font-size: 16px; font-weight: 800; margin: 0; color: #0F172A;">Recent AI Conversations</h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        mock_convs = [
            ("DIAGNOSTIC QUERY", "Potential anomalies in MRI Patient #882", "The AI identified a 3mm area of concern in the left..."),
            ("LAB COMPARISON", "Historical Blood Work Trend Analysis", "Comparing results from 2021 to current Q4 findings shows..."),
            ("DRUG INTERACTION", "Medication Cross-Reference Check", "No critical interactions found between prescribed Lisinopril...")
        ]
        for tag, title, snippet in mock_convs:
            st.markdown(
                f"""
                <div style="padding: 14px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #F1F5F9; margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: 800; color: #0D9488; text-transform: uppercase; margin-bottom: 4px;">{tag}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 2px;">{title}</div>
                    <div style="font-size: 12px; color: #64748B; font-style: italic;">"{snippet}"</div>
                </div>
                """,
                unsafe_allow_html=True
            )
