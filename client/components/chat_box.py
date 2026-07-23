import streamlit as st
from typing import List, Dict

def render_chat_message(role: str, content: str) -> None:
    """
    Renders a styled chat bubble for User vs. AI Assistant matching ChatGPT / Perplexity aesthetic.
    """
    if role == "user":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                <div style="background-color: #0055D4; color: white; padding: 14px 20px; border-radius: 20px 20px 4px 20px; max-width: 80%; font-size: 14px; box-shadow: 0 4px 12px rgba(0,85,212,0.15);">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 16px; align-items: flex-start; gap: 12px;">
                <div style="width: 36px; height: 36px; background-color: #0D9488; color: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 800; shrink: 0;">
                    🤖
                </div>
                <div style="background-color: #FFFFFF; color: #0F172A; border: 1px solid #E2E8F0; padding: 16px 22px; border-radius: 4px 20px 20px 20px; max-width: 82%; font-size: 14px; line-height: 1.6; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
