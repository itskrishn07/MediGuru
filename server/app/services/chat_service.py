import logging
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from prompts.chat_prompt import CHAT_PROMPT
from .retrieval_service import retrieve_relevant_chunks

logger = logging.getLogger(__name__)

def chat_with_records(query: str, document_ids: list[int] | None = None) -> str:
    """
    Answers a patient's question based on context retrieved from their medical records.
    """
    try:
        # 1. Retrieve context
        chunks = retrieve_relevant_chunks(query, n_results=4, document_ids=document_ids)
        context_text = "\n\n".join([f"--- Chunk from {c['metadata'].get('filename')} ---\n{c['text']}" for c in chunks])
        
        if not context_text:
            context_text = "No medical records found."

        # 2. Build prompt
        formatted_prompt = CHAT_PROMPT.format(context=context_text, question=query)
        
        # 3. Call LLM
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("API key required. Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
            
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, api_key=api_key)
        
        message = HumanMessage(content=formatted_prompt)
        response = llm.invoke([message])
        
        return response.content if response else "No response generated."
    except Exception as e:
        logger.error(f"Error in chat_with_records: {str(e)}", exc_info=True)
        return f"Sorry, I encountered an error while processing your request: {str(e)}"
