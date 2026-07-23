import streamlit as st

def render_stat_card(title: str, value: str, trend: str = "", icon: str = "📁") -> None:
    """
    Renders a styled KPI metric card matching the user's dashboard design.
    """
    trend_html = f'<span style="color: #10B981; font-weight: 700; font-size: 12px; background-color: #ECFDF5; padding: 2px 8px; border-radius: 6px;">{trend}</span>' if trend else ''
    st.markdown(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="width: 40px; height: 40px; background-color: #EFF6FF; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px;">
                    {icon}
                </div>
                {trend_html}
            </div>
            <div style="font-size: 12px; font-weight: 600; color: #64748B; margin-bottom: 4px;">{title}</div>
            <div style="font-size: 26px; font-weight: 800; color: #0F172A;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_banner_card(title: str, subtitle: str, bg_color: str = "blue", icon: str = "📤") -> None:
    """
    Renders a large quick-action banner card (Upload New Report / Start AI Chat).
    """
    bg_gradient = "linear-gradient(135deg, #0055D4 0%, #0044AB 100%)" if bg_color == "blue" else "linear-gradient(135deg, #0D9488 0%, #0F766E 100%)"
    st.markdown(
        f"""
        <div style="background: {bg_gradient}; color: white; border-radius: 20px; padding: 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 20px rgba(0,0,0,0.08);">
            <div>
                <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 4px; color: white;">{title}</h3>
                <p style="font-size: 13px; color: rgba(255,255,255,0.85); margin: 0;">{subtitle}</p>
            </div>
            <div style="width: 48px; height: 48px; background-color: rgba(255,255,255,0.2); backdrop-filter: blur(8px); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 22px;">
                {icon}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
