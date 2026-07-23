import streamlit as st
from typing import Optional, Any

def render_upload_box() -> Optional[Any]:
    """
    Renders a styled dropzone file upload box supporting PDF, PNG, JPG, JPEG files up to 25MB.
    Returns the uploaded file object.
    """
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 2px dashed #93C5FD; border-radius: 24px; padding: 32px; text-align: center; margin-bottom: 24px;">
            <div style="width: 64px; height: 64px; background-color: #EFF6FF; color: #0055D4; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 28px; margin-bottom: 16px;">
                ☁️
            </div>
            <h3 style="font-size: 18px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Drag and drop your files here</h3>
            <p style="font-size: 13px; color: #64748B; margin-bottom: 16px;">Supported formats: PDF, PNG, JPG, JPEG (Max 25MB)</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    uploaded_file = st.file_uploader(
        "Choose a medical document",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=False,
        label_visibility="collapsed"
    )
    return uploaded_file
