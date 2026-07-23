import streamlit as st
from services.auth_service import AuthService
from utils.session import login_user, logout_user

def is_logged_in() -> bool:
    """
    Checks if current session has an active authenticated state and access token.
    """
    return bool(st.session_state.get("authenticated", False) and st.session_state.get("access_token"))

def require_auth() -> bool:
    """
    Guards protected pages. If user is not authenticated, redirects to Login page.
    """
    if not is_logged_in():
        st.session_state["current_page"] = "Login"
        st.rerun()
        return False
    return True

def fetch_and_store_user_profile() -> None:
    """
    Retrieves current user details from backend and updates session state.
    """
    if is_logged_in() and not st.session_state.get("user_info"):
        success, profile = AuthService.get_current_user()
        if success:
            st.session_state["user_info"] = profile
