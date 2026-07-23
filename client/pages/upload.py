import streamlit as st
from services.upload_service import UploadService
from components.upload_box import render_upload_box
from components.loading import render_processing_pipeline

def render_upload_page() -> None:
    """
    Renders the Upload Medical Reports page matching the clinical user design.
    """
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Upload Medical Reports</h1>
            <p style="font-size: 14px; color: #64748B;">Securely upload your scans, blood tests, or clinical notes for AI-powered analysis.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([7, 5])

    with col1:
        # File Dropzone
        uploaded_file = render_upload_box()

        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type or "application/pdf"

            st.info(f"📁 Selected: **{file_name}** ({len(file_bytes) / 1024:.1f} KB)")

            if st.button("🚀 Process & Analyze Document", use_container_width=True, type="primary"):
                # Render multi-stage processing pipeline animation
                render_processing_pipeline(file_name)

                # Send file bytes to backend POST /upload API
                success, result = UploadService.upload_document(file_name, file_bytes, content_type)

                if success:
                    st.success("Document analyzed & indexed successfully!")
                    doc_id = result.get("document_id")
                    if doc_id:
                        st.session_state["selected_report_id"] = doc_id
                        st.session_state["current_page"] = "Report Details"
                        st.rerun()
                    else:
                        st.session_state["current_page"] = "Reports"
                        st.rerun()
                else:
                    st.error(f"Upload failed: {result}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Recent Uploads Preview List
        st.markdown("<h3 style='font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 12px;'>Recent Uploads</h3>", unsafe_allow_html=True)
        recent_items = [
            ("Chest_Xray_012.png", "2 mins ago • 3.4 MB", "Ready for Analysis"),
            ("Blood_Work_Nov23.pdf", "1 hour ago • 1.2 MB", "Ready for Analysis")
        ]
        for fname, meta, status in recent_items:
            st.markdown(
                f"""
                <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 13px; font-weight: 700; color: #0F172A;">📄 {fname}</div>
                        <div style="font-size: 11px; color: #94A3B8;">{meta}</div>
                    </div>
                    <span class="badge-success">• {status}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        # Right Info Panel: Upload Tips
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 24px; margin-bottom: 20px;">
                <h3 style="font-size: 16px; font-weight: 800; color: #0055D4; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                    💡 Upload Tips
                </h3>
                <ul style="font-size: 13px; color: #475569; padding-left: 20px; line-height: 1.6;">
                    <li style="margin-bottom: 10px;">Ensure good lighting for photos to minimize shadows and glare.</li>
                    <li style="margin-bottom: 10px;">Flatten documents for better OCR accuracy and character recognition.</li>
                    <li style="margin-bottom: 10px;">High resolution scans (300dpi+) are recommended for complex reports.</li>
                </ul>
                <hr style="border: 0; border-top: 1px solid #F1F5F9; margin: 16px 0;">
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px;">
                    <div style="font-size: 12px; font-weight: 700; color: #0F172A; margin-bottom: 2px;">Privacy Note</div>
                    <div style="font-size: 11px; color: #64748B;">All medical documents are encrypted (AES-256) and handled in accordance with HIPAA compliance standards.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Fast AI Processing Banner
        st.markdown(
            """
            <div class="banner-blue">
                <h4 style="font-size: 16px; font-weight: 800; margin-bottom: 4px; color: white;">Fast AI Processing</h4>
                <p style="font-size: 12px; color: #DBEAFE; margin: 0;">Most reports are analyzed within 30-60 seconds after upload.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
