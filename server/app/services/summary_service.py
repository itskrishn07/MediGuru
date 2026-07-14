import logging
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from prompts.summary_prompt import SUMMARY_PROMPT

logger = logging.getLogger(__name__)

def summarize_document(text: str) -> str:
    """
    Summarizes the extracted document text using Gemini.
    """
    if not text or not text.strip():
        return "No text available to summarize."
        
    try:
        formatted_prompt = SUMMARY_PROMPT.format(document_text=text)
        
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("API key required. Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
            
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, api_key=api_key)
        
        message = HumanMessage(content=formatted_prompt)
        response = llm.invoke([message])
        
        return response.content if response else "No summary generated."
    except Exception as e:
        logger.error(f"Error in summarize_document: {str(e)}", exc_info=True)
        return f"Summary generation failed: {str(e)}"
