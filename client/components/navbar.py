import streamlit as st

def render_top_navbar() -> None:
    """
    Renders top navigation header bar with search box and user badge.
    """
    st.markdown(
        """
        <div style="background: white; border-bottom: 1px solid #E2E8F0; padding: 12px 24px; margin-bottom: 24px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: 800; color: #0055D4; font-size: 16px;">MedAI Analyzer Pro</div>
            <div style="font-size: 12px; color: #64748B;">Clinical Data Intelligence Platform</div>
        </div>
        """,
        unsafe_allow_html=True
    )
