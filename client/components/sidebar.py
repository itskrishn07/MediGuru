import streamlit as st
from utils.constants import APP_NAME
from utils.session import logout_user

def render_sidebar() -> str:
    """
    Renders a modern, professional SaaS navigation sidebar matching the design.
    Returns the selected page string.
    """
    with st.sidebar:
        # Branding
        st.markdown(
            f"""
            <div style="display: flex; items-center; gap: 12px; margin-bottom: 24px; padding-left: 8px;">
                <div style="background-color: #0055D4; color: white; width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; box-shadow: 0 4px 10px rgba(0,85,212,0.25);">
                    🏥
                </div>
                <div>
                    <div style="font-size: 16px; font-weight: 800; color: #0F172A; line-height: 1.2;">
                        {APP_NAME}
                    </div>
                    <div style="font-size: 11px; font-weight: 600; color: #64748B;">
                        Analyzer Pro
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Primary Action Button
        if st.button("➕ New Analysis", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Upload"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; padding-left: 8px;'>Navigation</p>", unsafe_allow_html=True)

        pages = [
            ("Dashboard", "📊 Dashboard"),
            ("Reports", "📑 Medical Reports"),
            ("Upload", "📤 Upload Report"),
            ("Chat", "🤖 AI Medical Chat"),
            ("Compare Reports", "⚖️ Compare Reports"),
            ("Profile", "👤 User Profile"),
            ("Settings", "⚙️ System Settings")
        ]

        current_page = st.session_state.get("current_page", "Dashboard")

        for page_id, page_label in pages:
            button_type = "primary" if current_page == page_id else "secondary"
            if st.button(page_label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state["current_page"] = page_id
                st.rerun()

        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("---")

        # User profile summary at bottom of sidebar
        user_info = st.session_state.get("user_info", {})
        user_name = user_info.get("full_name", "Dr. Sarah Smith") if isinstance(user_info, dict) else "Dr. Sarah Smith"
        
        st.markdown(
            f"""
            <div style="padding: 8px; margin-bottom: 12px;">
                <div style="font-size: 13px; font-weight: 700; color: #0F172A;">{user_name}</div>
                <div style="font-size: 11px; color: #64748B;">NEUROLOGIST</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🚪 Log Out", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()

    return st.session_state.get("current_page", "Dashboard")
