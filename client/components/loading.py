import time
import streamlit as st

def render_processing_pipeline(file_name: str) -> None:
    """
    Renders a multi-stage visual AI pipeline loader:
    1. Uploading file...
    2. Running PaddleOCR text extraction...
    3. Extracting structured medical information via Gemini...
    4. Generating patient summary...
    5. Saving to PostgreSQL & ChromaDB vector store...
    """
    st.markdown(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Processing {file_name}</h3>
            <p style="font-size: 13px; color: #64748B; margin-bottom: 16px;">Our AI pipeline is processing your medical document.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    stages = [
        ("📤 Step 1/5: Uploading document securely...", 0.2),
        ("🔍 Step 2/5: Running PaddleOCR & text extraction...", 0.4),
        ("🤖 Step 3/5: Extracting medical entities with Gemini 2.5 Flash...", 0.6),
        ("📝 Step 4/5: Generating patient-friendly summary...", 0.8),
        ("💾 Step 5/5: Indexing embeddings in ChromaDB vector store...", 1.0)
    ]

    progress_bar = st.progress(0.0)
    status_text = st.empty()

    for stage_msg, progress_val in stages:
        status_text.markdown(f"**{stage_msg}**")
        progress_bar.progress(progress_val)
        time.sleep(0.4)

    status_text.markdown("✅ **Processing complete! Directing to Report Details...**")
