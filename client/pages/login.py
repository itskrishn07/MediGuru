import streamlit as st
from services.auth_service import AuthService
from utils.session import login_user
from utils.constants import APP_NAME, APP_TAGLINE

def render_login_page() -> None:
    """
    Renders a modern, SaaS-style login page matching the medical theme.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Card Container
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; padding: 40px; border-radius: 24px; border: 1px solid #E2E8F0; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);">
                <div style="text-align: center; margin-bottom: 24px;">
                    <div style="display: inline-block; background-color: #0055D4; color: white; padding: 12px 18px; border-radius: 16px; font-weight: 800; font-size: 20px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,85,212,0.3);">
                        🏥 {APP_NAME}
                    </div>
                    <h2 style="font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">Welcome Back</h2>
                    <p style="font-size: 14px; color: #64748B;">Sign in to access your AI medical intelligence dashboard</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.form(key="login_form", clear_on_submit=False):
            email = st.text_input("Work Email", placeholder="sarah.j@clinic.ai", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            
            remember_me = st.checkbox("Remember me on this device", value=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_button:
                if not email.strip() or not password:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Authenticating credentials with secure server..."):
                        success, res = AuthService.login(email.strip(), password)
                        if success:
                            token = res.get("access_token")
                            refresh_token = res.get("refresh_token", "")
                            
                            # Retrieve user details
                            login_user(token, refresh_token, {"email": email})
                            
                            # Attempt to fetch full profile
                            user_success, user_data = AuthService.get_current_user()
                            if user_success:
                                st.session_state["user_info"] = user_data
                                
                            st.success("Authentication successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error(f"Login Failed: {res}")
                            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center; font-size: 14px; color: #64748B;">
                Don't have an account? 
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Create an account", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "Register"
            st.rerun()
