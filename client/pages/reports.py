import streamlit as st
from services.report_service import ReportService

def render_reports_page() -> None:
    """
    Renders the Reports History page featuring report searching, filtering,
    viewing, and backend report deletion.
    """
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Medical Reports</h1>
            <p style="font-size: 14px; color: #64748B;">Manage, search, and analyze your processed patient document history.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Search and Filter Toolbar
    f_col1, f_col2 = st.columns([8, 4])
    with f_col1:
        search_term = st.text_input("Search reports by filename or patient name...", placeholder="e.g. John Doe, MRI, Blood Work", key="rep_search")
    with f_col2:
        status_filter = st.selectbox("Filter Status", ["All Statuses", "Analyzed", "Processing", "Flagged"])

    # Fetch Reports from backend
    success, reports_data = ReportService.get_all_reports()
    reports_list = reports_data if success and isinstance(reports_data, list) else []

    st.markdown("<br>", unsafe_allow_html=True)

    if reports_list:
        filtered = reports_list
        if search_term.strip():
            term = search_term.strip().lower()
            filtered = [r for r in filtered if term in r.get("filename", "").lower() or term in (r.get("patient_name") or "").lower()]

        st.markdown(f"Showing **{len(filtered)}** medical reports:")
        
        for rep in filtered:
            r_id = rep.get("id")
            fname = rep.get("filename", f"Report_{r_id}.pdf")
            pname = rep.get("patient_name", "Unknown Patient")
            created_at = str(rep.get("created_at", ""))[:10]

            col_a, col_b, col_c, col_d = st.columns([5, 3, 2, 2])
            with col_a:
                st.markdown(f"📄 **{fname}**\n\n<span style='font-size:12px; color:#64748B;'>Patient: {pname}</span>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"📅 **Date:** {created_at}")
            with col_c:
                if st.button("Open Report", key=f"open_{r_id}", use_container_width=True):
                    st.session_state["selected_report_id"] = r_id
                    st.session_state["current_page"] = "Report Details"
                    st.rerun()
            with col_d:
                if st.button("🗑️ Delete", key=f"del_{r_id}", use_container_width=True):
                    del_success, del_res = ReportService.delete_report(r_id)
                    if del_success:
                        st.success(f"Deleted report #{r_id}")
                        st.rerun()
                    else:
                        st.error(f"Could not delete report: {del_res}")
            st.divider()
    else:
        st.info("No uploaded reports found in database yet. Click 'Upload Report' to get started.")
