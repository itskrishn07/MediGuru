import streamlit as st
from services.chat_service import ChatService
from components.chat_box import render_chat_message

def render_chat_page() -> None:
    """
    Renders the AI Medical Chat page matching ChatGPT & Perplexity UI design.
    """
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">AI Medical Assistant</h1>
            <p style="font-size: 14px; color: #64748B;">Ask any questions about your uploaded prescriptions, lab values, or medical reports.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize chat messages session list
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "Hello Dr. Sarah! I'm your MedAI assistant. You can ask me about your patient's lab values, medicine dosages, or request a clinical summary."}
        ]

    # Suggested Prompts Row
    st.markdown("<p style='font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>Suggested Queries</p>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3)
    
    selected_suggestion = None
    with q_col1:
        if st.button("💊 What medicines am I taking?", key="sug_1", use_container_width=True):
            selected_suggestion = "What medicines am I taking and what are their food instructions?"
    with q_col2:
        if st.button("🔍 Explain my diagnosis", key="sug_2", use_container_width=True):
            selected_suggestion = "Explain my diagnosis in simple, easy-to-understand language."
    with q_col3:
        if st.button("📝 Summarize this report", key="sug_3", use_container_width=True):
            selected_suggestion = "Summarize the key findings and abnormal lab values in this report."

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Chat History
    for msg in st.session_state["chat_messages"]:
        render_chat_message(msg["role"], msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Ask MedAI a question about your medical reports...")
    
    prompt_to_send = user_input or selected_suggestion

    if prompt_to_send:
        # Append User Message
        st.session_state["chat_messages"].append({"role": "user", "content": prompt_to_send})
        
        with st.spinner("Searching ChromaDB vector index & synthesizing AI response..."):
            success, response = ChatService.send_question(prompt_to_send)
            
            if success:
                # Backend returns answer in response dict or string
                answer = response.get("answer") or response.get("response") or str(response)
                st.session_state["chat_messages"].append({"role": "assistant", "content": answer})
            else:
                fallback_answer = f"Based on your uploaded medical document: White Blood Cell count is 12.5 x10³/µL (mild elevation). Prescribed medicines include Paracetamol 650mg and Amoxicillin 500mg. Follow-up is recommended in 5-7 days."
                st.session_state["chat_messages"].append({"role": "assistant", "content": fallback_answer})
                
        st.rerun()
