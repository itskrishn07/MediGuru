import streamlit as st
import pandas as pd
from typing import List, Dict, Any

def render_reports_table(reports: List[Dict[str, Any]]) -> None:
    """
    Renders a styled pandas dataframe / html table of medical reports.
    """
    if not reports:
        st.info("No reports found.")
        return

    data = []
    for r in reports:
        data.append({
            "ID": r.get("id"),
            "Filename": r.get("filename", "Report.pdf"),
            "Patient": r.get("patient_name", "N/A"),
            "Created Date": str(r.get("created_at", ""))[:10]
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
