import streamlit as st
from services.auth_service import AuthService
from utils.constants import APP_NAME

def render_register_page() -> None:
    """
    Renders a clean, enterprise registration form matching the user's uploaded design.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; padding: 36px; border-radius: 24px; border: 1px solid #E2E8F0; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);">
                <div style="text-align: center; margin-bottom: 24px;">
                    <div style="display: inline-block; background-color: #0055D4; color: white; padding: 10px 16px; border-radius: 14px; font-weight: 800; font-size: 18px; margin-bottom: 12px;">
                        🏥 {APP_NAME}
                    </div>
                    <h2 style="font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Create an account</h2>
                    <p style="font-size: 14px; color: #64748B;">Start your 14-day free trial of enterprise medical analysis</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.form(key="register_form", clear_on_submit=False):
            full_name = st.text_input("Full Name", placeholder="Dr. Sarah Johnson", key="reg_name")
            email = st.text_input("Work Email", placeholder="sarah.j@clinic.ai", key="reg_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="reg_confirm_password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button("Register", use_container_width=True)
            
            if submit_button:
                if not full_name.strip():
                    st.error("Please enter your full name.")
                elif not email.strip():
                    st.error("Please enter a valid work email.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    with st.spinner("Creating user account..."):
                        success, res = AuthService.register(full_name.strip(), email.strip(), password)
                        if success:
                            st.success("Account created successfully! Redirecting to login...")
                            st.session_state["current_page"] = "Login"
                            st.rerun()
                        else:
                            st.error(f"Registration Failed: {res}")
                            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center; font-size: 14px; color: #64748B;">
                Already have an account?
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Back to Login", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "Login"
            st.rerun()
