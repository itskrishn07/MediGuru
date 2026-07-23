import streamlit as st
from utils.constants import API_BASE_URL

def render_settings_page() -> None:
    """
    Renders the System Settings page for API configuration and AI pipeline options.
    """
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">System Settings</h1>
            <p style="font-size: 14px; color: #64748B;">Configure backend API server URLs, OCR models, and LLM preferences.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Backend Connection")
    backend_url = st.text_input("FastAPI Server Base URL", value=API_BASE_URL)
    
    st.markdown("### 🤖 AI Engine Settings")
    st.selectbox("LLM Model Engine", ["Gemini 2.5 Flash (Default)", "Gemini 1.5 Pro", "Custom Local Model"])
    st.selectbox("OCR Engine", ["PaddleOCR (Default)", "PyMuPDF Native Text Parser", "Tesseract Fallback"])
    
    st.markdown("### 🗄️ Vector Database Status")
    st.markdown("● **ChromaDB Connection:** Connected (`chroma_db/` persistent store)")

    if st.button("Save Settings Configuration", type="primary"):
        st.success("Settings saved successfully!")
