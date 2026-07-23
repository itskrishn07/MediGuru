import streamlit as st
import sys
from pathlib import Path

# Add client folder to sys.path to enable smooth module imports
client_dir = Path(__file__).resolve().parent
if str(client_dir) not in sys.path:
    sys.path.insert(0, str(client_dir))

# Configure Streamlit page layout & favicon
st.set_page_config(
    page_title="MediGuru — Clinical Data Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Utilities, Session & Styling
from utils.session import init_session_state
from utils.styles import apply_custom_styles
from utils.auth import is_logged_in, fetch_and_store_user_profile

# Import Page Modules
from pages.login import render_login_page
from pages.register import render_register_page
from pages.dashboard import render_dashboard_page
from pages.upload import render_upload_page
from pages.reports import render_reports_page
from pages.report_details import render_report_details_page
from pages.chat import render_chat_page
from pages.compare_reports import render_compare_reports_page
from pages.profile import render_profile_page
from pages.settings import render_settings_page

# Import Components
from components.sidebar import render_sidebar

def main() -> None:
    """
    Main entry point for MediGuru Streamlit frontend application.
    Controls authentication guards, theme CSS injection, sidebar rendering, and page routing.
    """
    # 1. Initialize session state variables
    init_session_state()

    # 2. Inject custom SaaS CSS styles
    apply_custom_styles()

    # 3. Handle Authentication Routing
    if not is_logged_in():
        current_page = st.session_state.get("current_page", "Login")
        if current_page == "Register":
            render_register_page()
        else:
            render_login_page()
        return

    # User is logged in: fetch profile details if missing
    fetch_and_store_user_profile()

    # 4. Render Sidebar Navigation for authenticated users
    selected_page = render_sidebar()

    # 5. Route to Active Page
    if selected_page == "Dashboard":
        render_dashboard_page()
    elif selected_page == "Upload":
        render_upload_page()
    elif selected_page == "Reports":
        render_reports_page()
    elif selected_page == "Report Details":
        render_report_details_page()
    elif selected_page == "Chat":
        render_chat_page()
    elif selected_page == "Compare Reports":
        render_compare_reports_page()
    elif selected_page == "Profile":
        render_profile_page()
    elif selected_page == "Settings":
        render_settings_page()
    else:
        render_dashboard_page()

if __name__ == "__main__":
    main()
