import streamlit as st
from typing import Optional, Dict, Any

def init_session_state() -> None:
    """
    Initializes Streamlit session state keys for authentication and app navigation.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "access_token" not in st.session_state:
        st.session_state["access_token"] = None
    if "refresh_token" not in st.session_state:
        st.session_state["refresh_token"] = None
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = None
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Login"
    if "selected_report_id" not in st.session_state:
        st.session_state["selected_report_id"] = None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

def login_user(access_token: str, refresh_token: str, user_info: Dict[str, Any]) -> None:
    """
    Sets session state upon successful user authentication.
    """
    st.session_state["authenticated"] = True
    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token
    st.session_state["user_info"] = user_info
    st.session_state["current_page"] = "Dashboard"

def logout_user() -> None:
    """
    Clears user session state on logout.
    """
    st.session_state["authenticated"] = False
    st.session_state["access_token"] = None
    st.session_state["refresh_token"] = None
    st.session_state["user_info"] = None
    st.session_state["selected_report_id"] = None
    st.session_state["chat_history"] = []
    st.session_state["current_page"] = "Login"

def get_auth_header() -> Dict[str, str]:
    """
    Returns Authorization header dictionary for authenticated API requests.
    """
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}
