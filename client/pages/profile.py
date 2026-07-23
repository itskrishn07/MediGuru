import streamlit as st
from utils.session import logout_user
from services.report_service import ReportService

def render_profile_page() -> None:
    """
    Renders the User Profile page detailing account information, reports uploaded, and session actions.
    """
    user_info = st.session_state.get("user_info", {})
    user_name = user_info.get("full_name", "Dr. Sarah Smith") if isinstance(user_info, dict) else "Dr. Sarah Smith"
    user_email = user_info.get("email", "sarah.j@clinic.ai") if isinstance(user_info, dict) else "sarah.j@clinic.ai"

    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">User Profile</h1>
            <p style="font-size: 14px; color: #64748B;">Manage your account credentials and system authorization.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([7, 5])

    with col1:
        st.markdown(
            f"""
            <div style="background: white; padding: 28px; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
                    <div style="width: 64px; height: 64px; border-radius: 50%; background-color: #0055D4; color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800;">
                        👩‍⚕️
                    </div>
                    <div>
                        <h2 style="font-size: 20px; font-weight: 800; color: #0F172A; margin: 0;">{user_name}</h2>
                        <p style="font-size: 13px; color: #64748B; margin: 2px 0 0 0;">Senior Neurologist • Clinical Specialist</p>
                    </div>
                </div>

                <hr style="border: 0; border-top: 1px solid #F1F5F9; margin: 20px 0;">

                <div style="font-size: 14px; line-height: 2.2;">
                    <div><strong>Work Email:</strong> {user_email}</div>
                    <div><strong>Account Role:</strong> Medical Practitioner (Enterprise Tier)</div>
                    <div><strong>Organization:</strong> St. Jude Medical Center</div>
                    <div><strong>Security Standard:</strong> HIPAA Compliant • AES-256 Encrypted</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="background: white; padding: 24px; border-radius: 20px; border: 1px solid #E2E8F0;">
                <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Quick Actions</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚪 Logout from Session", type="primary", use_container_width=True):
            logout_user()
            st.rerun()
